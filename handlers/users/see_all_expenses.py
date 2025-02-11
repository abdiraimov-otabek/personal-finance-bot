from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os

from loader import db
from keyboards.inline.buttons import download_expenses_data
from utils.pgtoexcel import export_to_excel
from utils.extra_datas import format_amount

router = Router()


@router.message(F.text == "📊 Xarajatlarni ko‘rish")
async def ask_expense_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        total_expenses = await db.select_all_expenses(user_id=user_id)

        if total_expenses is not None:
            await message.answer(
                f"💸 Barcha xarajatlaringizning jami miqdori: {format_amount(total_expenses)} so'm",
                reply_markup=download_expenses_data,
            )
        else:
            await message.axnswer("Hozircha xarajatlar yo'q 🤷‍♂️")
    except Exception as e:
        print(f"Error while fetching expenses: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos qayta urinib ko'ring ❌")


@router.callback_query(F.data == "get_excel_file_expenses")
async def get_excel_file(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id

        expenses = await db.select_all_expenses_file(user_id)

        if not expenses:
            await callback.answer("Xarajatlar mavjud emas! ❌")
            return

        data = [
            (
                str(e["id"]),
                str(e["amount"]),
                e["reason"],
                e["date"].strftime("%Y-%m-%d"),
            )
            for e in expenses
        ]

        file_path = "data/xarajatlar_royxati.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        await export_to_excel(
            data=data,
            headings=["ID", "Miqdor", "Sabab", "Kun"],
            filepath=file_path,
        )

        await callback.message.answer_document(types.input_file.FSInputFile(file_path))

        await callback.answer("Hisobot yuborildi ✅")

    except Exception as e:
        print(f"Error while generating Excel file: {e}")
        await callback.answer("Xatolik yuz berdi. Iltimos qayta urinib ko'ring ❌")
