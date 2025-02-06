from aiogram.filters import BaseFilter
from aiogram.types import Message
from loader import db


class IsPremiumUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        query = "SELECT is_premium FROM users WHERE telegram_id = $1"
        result = await db.execute(query, user_id, fetchrow=True)
        if result and result["is_premium"]:
            return True
        return False
