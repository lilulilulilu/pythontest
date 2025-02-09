import functools
import time
from typing import Callable, Any
def async_timed():
    def wrapper (func: Callable) -> Callable:
        @functools.wraps(func) 
        async def wrapped (*args, **kwargs) -> Any:
            print (f'starting (func) with args fargs) (kwargs)') 
            start = time.time ()
            try:
                return await func(*args, **kwargs) 
            finally:
                end = time.time()
                total = end - start
                print(f'finished {func} in {total:.4f} second(s)") return wrapped')
        return wrapped
    return wrapper


import asyncio
@async_timed ()
async def delay (delay_seconds: int) -> int:
    print (f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print (f'finished sleeping for {delay_seconds} second(s) ')
    return delay_seconds

@async_timed()
async def main () :
    task_one = asyncio.create_task(delay(2)) 
    task_two = asyncio.create_task(delay(3))
    await task_one 
    await task_two
    
asyncio.run(main())