from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import Bot

CHANNEL_USERNAME = "@otabekabdiraimov_blog"


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot  # Bot obyektini middleware ichiga olamiz

    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id

        try:
            chat_member = await self.bot.get_chat_member(CHANNEL_USERNAME, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton(
                        "Obuna bo'ling", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
                    )
                )
                await message.answer(
                    "⚠️ Botni ishlatish uchun quyidagi kanalga obuna bo'ling.",
                    reply_markup=markup,
                )
                raise Exception("User not subscribed")
        except Exception as e:
            await message.answer("⚠️ Xatolik!")
            raise e  # Stop processing
