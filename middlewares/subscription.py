from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types

CHANNEL_USERNAME = "@otabekabdiraimov_blog"


class SubscriptionMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        bot = message.bot

        # Check if user is subscribe
        try:
            chat_member = await bot.get_chat_member(
                chat_id=CHANNEL_USERNAME, user_id=user_id
            )
            if chat_member.status not in ["member", "administrator", "creator"]:
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(
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
