from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os

from loader import db
from keyboards.inline.buttons import download_incomes_data
from utils.pgtoexcel import export_to_excel
from utils.extra_datas import format_amount

router = Router()


@router.message(F.text == "📈 Daromadlarni ko‘rish")
async def ask_income_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        total_incomes = await db.select_all_incomes(user_id=user_id)

        if total_incomes is not None:
            await message.answer(
                f"💰 Barcha daromadlaringizning jami miqdori: {format_amount(total_incomes)} so'm",
                reply_markup=download_incomes_data,
            )
        else:
            await message.answer("Hozircha daromadlar yo'q 🤷‍♂️")
    except Exception as e:
        print(f"Error while fetching incomes: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos qayta urinib ko'ring ❌")


@router.callback_query(F.data == "get_excel_file_incomes")
async def get_excel_file(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id

        incomes = await db.select_all_incomes_file(user_id)

        if not incomes:
            await callback.answer("Daromadlar mavjud emas! ❌")
            return

        data = [
            (
                str(i["id"]),
                str(i["amount"]),
                i["reason"],
                i["date"].strftime("%Y-%m-%d"),
            )
            for i in incomes
        ]

        file_path = "data/daromadlar_royxati.xlsx"
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
