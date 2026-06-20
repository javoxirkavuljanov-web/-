import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db
from handlers import start_router, expense_router, income_router, statistics_router

logging.basicConfig(level=logging.INFO)


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(expense_router)
    dp.include_router(income_router)
    dp.include_router(statistics_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
