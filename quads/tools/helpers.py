import asyncio


def get_running_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop()
    if not loop.is_running():
        raise RuntimeError("The object should be created within an async function")
    return loop
