import asyncio
import uvicorn

from fastapi import Depends, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from connection.manager import ConnectionManager
from api import admin
from dependencies.token import get_token_header

app = FastAPI()
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
)

manager = ConnectionManager()

templates = Jinja2Templates(directory="static/templates")

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """Handle websocket connections and broadcast messages to all connected clients."""
    await manager.connect(websocket, username)
    try:
        while True:
            data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
            message = f"{manager.usernames[websocket]}: {data}"
            await manager.broadcast(message)
    except asyncio.TimeoutError:
        manager.disconnect(websocket)
        print(f"{username} timed out.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"{username} disconnected.")
    except Exception as e:
        manager.disconnect(websocket)
        print(f"Error: {e}")



@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    """This is a web page for testing the websocket_endpoint.""" 
    return templates.TemplateResponse("index.html", {"request" : request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)