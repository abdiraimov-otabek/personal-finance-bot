import asyncio
import logging

from aiogram import Bot, Dispatcher
from loader import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def database_connected():
    """Ma'lumotlar bazasini yaratish"""
    await db.create()
    await db.create_table_users()
    await db.create_table_expense()
    await db.create_table_income()


async def setup_aiogram(dispatcher: Dispatcher, bot: Bot) -> None:
    """Botni sozlash"""
    from handlers import setup_routers
    from middlewares.throttling import ThrottlingMiddleware
    from filters import ChatPrivateFilter

    logger.info("Configuring aiogram")
    dispatcher.include_router(setup_routers())
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))
    dispatcher.message.filter(ChatPrivateFilter(chat_type=["private"]))
    logger.info("Configured aiogram")


async def on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    """Bot ishga tushganda bajariladigan kodlar"""
    from utils.set_bot_commands import set_default_commands
    from utils.notify_admins import on_startup_notify

    logger.info("Connecting to database...")
    await database_connected()

    logger.info("Deleting old webhook (if exists)")
    await bot.delete_webhook(drop_pending_updates=True)

    await setup_aiogram(dispatcher=dispatcher, bot=bot)
    await on_startup_notify(bot=bot)
    await set_default_commands(bot=bot)

    logger.info("Bot successfully started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    """Bot to‘xtaganda bajariladigan kodlar"""
    logger.info("Stopping bot...")
    await bot.session.close()
    await dispatcher.storage.close()


def main():
    """Botni ishga tushirish"""
    from data.config import BOT_TOKEN
    from aiogram.enums import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage

    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    asyncio.run(dispatcher.start_polling(bot, close_bot_session=True))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped!")
