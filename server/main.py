import asyncio
from server import init_message_handling_routine


if __name__ == '__main__':
    asyncio.run(init_message_handling_routine())

