from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import Bot, types

CHANNEL_USERNAME = "@otabekabdiraimov_blog"


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot  # Bot obyektini saqlaymiz

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id

        try:
            chat_member = await self.bot.get_chat_member(CHANNEL_USERNAME, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(
                        "Obuna bo'ling", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
                    )
                )
                await event.answer(
                    "⚠️ Botni ishlatish uchun quyidagi kanalga obuna bo'ling.",
                    reply_markup=markup,
                )
                return  # Agar user a'zo bo'lmasa, boshqa handlerlar ishlamasin
        except Exception as e:
            await event.answer("⚠️ Xatolik yuz berdi!")
            return

        return await handler(event, data)  # Agar a'zo bo'lsa, davom ettiramiz
