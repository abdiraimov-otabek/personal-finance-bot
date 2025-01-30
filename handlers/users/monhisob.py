from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.inline.buttons import choise_data
from states import ExpenseState

router = Router()


@router.message(F.text == "💰 Xarajat kiritish")
async def ask_expense_amount(message: Message, state: FSMContext):
    await message.answer("Xarajat miqdorini kiriting:")
    await state.set_state(ExpenseState.amount)
    # await message.edit_reply_markup(reply_markup=None)




@router.message(ExpenseState.amount)
async def get_expense_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():  # Faqat raqam kiritilganligini tekshiramiz
        await message.answer("Xarajat miqdori raqam bo‘lishi kerak! Qayta kiriting:")
        return
    await state.update_data(amount=message.text)
    await message.answer("Sabab kiriting?")
    await state.set_state(ExpenseState.reason)

@router.message(ExpenseState.reason)
async def get_expense_reason(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)

    today_date = datetime.now().strftime("%Y-%m-%d")

    await message.answer(f"Xarajat sanasi: {today_date}\nBu sanani ishlatamizmi?", reply_markup=choise_data)
    await state.set_state(ExpenseState.date_confirmation)


@router.callback_query(ExpenseState.date_confirmation, F.data == "yes")
async def confirm_date(callback_query, state: FSMContext):
    user_data = await state.get_data()
    expense_text = (f"✅ Xarajat kiritildi:\n"
                    f"💰 Miqdor: {user_data['amount']} so‘m\n"
                    f"📄 Sabab: {user_data['reason']}\n"
                    f"📅 Sana: {datetime.now().strftime('%Y-%m-%d')}")

    await callback_query.message.edit_reply_markup(reply_markup=None)

    await callback_query.message.answer(expense_text)
    await state.clear()


@router.callback_query(ExpenseState.date_confirmation, F.data == "no")
async def ask_new_date(callback_query, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer("Yangi sanani `YYYY-MM-DD` formatida kiriting:")
    await state.set_state(ExpenseState.new_date)


@router.message(ExpenseState.new_date)
async def get_new_date(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%Y-%m-%d")
        await state.update_data(date=message.text)

        user_data = await state.get_data()
        expense_text = (f"✅ Xarajat kiritildi:\n"
                        f"💰 Miqdor: {user_data['amount']} so‘m\n"
                        f"📄 Sabab: {user_data['reason']}\n"
                        f"📅 Sana: {user_data['date']}")

        await message.answer(expense_text)
        await state.clear()
    except ValueError:
        await message.answer("Noto‘g‘ri format! Iltimos, sanani `YYYY-MM-DD` formatida kiriting:")
