from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime
import re

from loader import db
from states import IncomeState
from utils.extra_datas import format_amount
from keyboards.inline.buttons import choise_data, income_categories

router = Router()


def validate_amount(amount_str: str) -> float:
    amount_str = amount_str.replace(" ", "")

    if not re.match(r"^\d{1,3}(?:\d{3})*(?:\.\d{1,2})?$", amount_str):
        raise ValueError(
            "⚠️ Xarajat miqdori noto‘g‘ri formatda! Raqamlar to‘g‘ri kiriting."
        )

    amount = float(amount_str)

    if amount < 1000:
        raise ValueError("⚠️ Daromad miqdori minimal 1000 bo‘lishi kerak!")

    return amount


# Start income entry flow
@router.message(F.text == "📥 Daromad kiritish")
async def start_income_entry(message: Message, state: FSMContext):
    await message.answer("Daromad miqdorini kiriting:\n\nMisol uchun: 100 000")
    await state.set_state(IncomeState.amount)


# Handle amount input
@router.message(IncomeState.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = validate_amount(message.text)
        await state.update_data(amount=amount)
        await message.answer(
            "Quyidagi sabablardan birini tanlang:", reply_markup=income_categories
        )
        await state.set_state(IncomeState.reason)
    except ValueError as e:
        await message.answer(str(e))


# Handle category selection via inline buttons
@router.callback_query(IncomeState.reason, F.data.startswith("income_"))
async def process_reason(callback: CallbackQuery, state: FSMContext):
    # Extract reason from callback data (remove "income_" prefix)
    reason = callback.data.split("_", 1)[1]
    await state.update_data(reason=reason)

    # Prepare date confirmation message
    today_date = datetime.now().strftime("%Y-%m-%d")
    await callback.message.edit_reply_markup()  # Clear category keyboard
    await callback.message.answer(
        f"📅 Daromad sanasi: {today_date}\nBu sanani ishlatamizmi?",
        reply_markup=choise_data,
    )
    await state.set_state(IncomeState.date_confirmation)
    await callback.answer()


# Handle date confirmation
@router.callback_query(IncomeState.date_confirmation, F.data == "yes")
async def confirm_current_date(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    current_date = datetime.now().date()

    # Save to database
    await db.add_income(
        amount=user_data["amount"],
        reason=user_data["reason"],
        date=current_date,
        user_id=callback.from_user.id,
    )

    # Format confirmation message
    income_text = (
        f"✅ Daromad kiritildi:\n"
        f"💰 Miqdor: {format_amount(user_data['amount'])} so'm\n"
        f"📄 Sabab: {user_data['reason']}\n"
        f"📅 Sana: {current_date}"
    )

    await callback.message.edit_reply_markup()  # Clear confirmation keyboard
    await callback.message.answer(income_text)
    await state.clear()


# Handle date change request
@router.callback_query(IncomeState.date_confirmation, F.data == "no")
async def request_new_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # Clear confirmation keyboard
    await callback.message.answer("Yangi sanani `YYYY-MM-DD` formatida kiriting:")
    await state.set_state(IncomeState.new_date)
    await callback.answer()


# Process custom date input
@router.message(IncomeState.new_date)
async def process_custom_date(message: Message, state: FSMContext):
    try:
        # Validate date format
        date_obj = datetime.strptime(message.text, "%Y-%m-%d").date()
        user_data = await state.get_data()

        # Save to database
        await db.add_income(
            amount=user_data["amount"],
            reason=user_data["reason"],
            date=date_obj,
            user_id=message.from_user.id,
        )

        # Format confirmation message
        income_text = (
            f"✅ Daromad kiritildi:\n"
            f"💰 Miqdor: {format_amount(user_data['amount'])} so'm\n"
            f"📄 Sabab: {user_data['reason']}\n"
            f"📅 Sana: {date_obj}"
        )

        await message.answer(income_text)
        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Noto‘g‘ri format! Iltimos, sanani `YYYY-MM-DD` formatida kiriting:"
        )
