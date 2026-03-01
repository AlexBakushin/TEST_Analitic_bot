import asyncio
from aiogram import Bot, Dispatcher
from application.handlers import router
from database import init_db, load_json_to_db
import os
from dotenv import load_dotenv

load_dotenv()
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Бот останавливается...")
    finally:
        await bot.session.close()
        print("Бот успешно остановлен")


if __name__ == "__main__":
    asyncio.run(init_db())
    print("БД инициализирована")
    asyncio.run(load_json_to_db("videos.json"))
    print("Данные импортированы")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
