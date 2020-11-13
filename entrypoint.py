import asyncio

from app.main import main


if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(main())
