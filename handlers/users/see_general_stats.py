from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loader import db
from utils.extra_datas import format_amount


router = Router()


@router.message(F.text == "💡 Umumiy statistikani ko‘rish")
async def ask_income_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        total_stats = await db.get_general_stat(user_id=user_id)

        if total_stats is not None:
            await message.answer(
                f"💰 Umumiy  statistika: {format_amount(total_stats)} so'm",
            )
        else:
            await message.answer("Hozircha statistika yo'q 🤷‍♂️")
    except Exception as e:
        print(f"Error while fetching incomes: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos qayta urinib ko'ring ❌")
