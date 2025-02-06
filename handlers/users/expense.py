from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime
import re
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

from loader import db
from states import ExpenseState
from utils.extra_datas import format_amount
from filters.is_premium_user import IsPremiumUser
from keyboards.inline.buttons import choise_data, expense_categories

router = Router()


def validate_amount(amount_str: str) -> float:
    amount_str = amount_str.replace(" ", "")
    if not re.match(r"^\d{1,3}(?:\d{3})*(?:\.\d{1,2})?$", amount_str):
        raise ValueError(
            "⚠️ Xarajat miqdori noto‘g‘ri formatda! Raqamlar to‘g‘ri kiriting."
        )
    amount = float(amount_str)
    if amount < 1000:
        raise ValueError("⚠️ Xarajat miqdori minimal 1000 bo‘lishi kerak!")
    return amount


@router.message(F.text == "💰 Xarajat kiritish")
async def start_expense_entry(message: Message, state: FSMContext):
    await message.answer("Xarajat miqdorini kiriting:\n\nMisol uchun: 100 000")
    await state.set_state(ExpenseState.amount)


@router.message(ExpenseState.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = validate_amount(message.text)
        await state.update_data(amount=amount)
        await message.answer(
            "Quyidagi sabablardan birini tanlang:", reply_markup=expense_categories
        )
        await state.set_state(ExpenseState.reason)
    except ValueError as e:
        await message.answer(str(e))


@router.callback_query(ExpenseState.reason, F.data.startswith("expense_"))
async def process_reason(callback: CallbackQuery, state: FSMContext):
    reason = callback.data.split("_", 1)[1]
    await state.update_data(reason=reason)
    today_date = datetime.now().strftime("%Y-%m-%d")
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        f"📅 Xarajat sanasi: {today_date}\nBu sanani ishlatamizmi?",
        reply_markup=choise_data,
    )
    await state.set_state(ExpenseState.date_confirmation)
    await callback.answer()


@router.callback_query(ExpenseState.date_confirmation, F.data == "yes")
async def confirm_current_date(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    current_date = datetime.now().date()
    await db.add_expense(
        amount=user_data["amount"],
        reason=user_data["reason"],
        date=current_date,
        user_id=callback.from_user.id,
    )
    expense_text = (
        f"✅ Xarajat kiritildi:\n"
        f"💰 Miqdor: {format_amount(user_data['amount'])} so'm\n"
        f"📄 Sabab: {user_data['reason']}\n"
        f"📅 Sana: {current_date}"
    )
    await callback.message.edit_reply_markup()
    await callback.message.answer(expense_text)
    await state.clear()


@router.callback_query(ExpenseState.date_confirmation, F.data == "no")
async def request_new_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Yangi sanani `YYYY-MM-DD` formatida kiriting:")
    await state.set_state(ExpenseState.new_date)
    await callback.answer()


@router.message(ExpenseState.new_date)
async def process_custom_date(message: Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, "%Y-%m-%d").date()
        user_data = await state.get_data()
        await db.add_expense(
            amount=user_data["amount"],
            reason=user_data["reason"],
            date=date_obj,
            user_id=message.from_user.id,
        )
        expense_text = (
            f"✅ Xarajat kiritildi:\n"
            f"💰 Miqdor: {format_amount(user_data['amount'])} so'm\n"
            f"📄 Sabab: {user_data['reason']}\n"
            f"📅 Sana: {date_obj}"
        )
        await message.answer(expense_text)
        await state.clear()
    except ValueError:
        await message.answer(
            "❌ Noto‘g‘ri format! Iltimos, sanani `YYYY-MM-DD` formatida kiriting:"
        )


@router.message(
    F.text == "🌟 Analitikani ko'rish (Jadval ko'rinishida)", IsPremiumUser()
)
async def send_statistics(message: Message):
    user_id = message.from_user.id
    try:
        categories_data = await db.get_category_stats(user_id=user_id)
        if not categories_data:
            await message.answer("📭 Hozircha xarajatlar mavjud emas!")
            return
        labels = [item["reason"] for item in categories_data]
        amounts = [float(item["total"]) for item in categories_data]
        total = sum(amounts)
        avg = total / len(amounts) if len(amounts) > 0 else 0
        top_category = labels[amounts.index(max(amounts))] if amounts else "Yo'q"
        plt.style.use("dark_background")
        fig = plt.figure(figsize=(14, 8), facecolor="#0F172A")
        ax = fig.add_subplot(111, facecolor="#0F172A")
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        gradient = np.vstack((gradient, gradient))
        ax.imshow(
            gradient,
            aspect="auto",
            cmap=plt.cm.Blues_r,
            alpha=0.1,
            extent=[0, len(labels), 0, max(amounts) * 1.2],
        )
        x_pos = np.arange(len(labels))
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(labels)))
        bars = ax.bar(
            x_pos,
            amounts,
            width=0.6,
            color=colors,
            edgecolor="#1E293B",
            linewidth=1.5,
            alpha=0.9,
        )
        for bar in bars:
            bar.set_hatch(".....")
            bar.set_edgecolor("#334155")
        for i, (label, value) in enumerate(zip(labels, amounts)):
            ax.text(
                i,
                value + max(amounts) * 0.02,
                f"⬆ {format_amount(value)}",
                color="#E2E8F0",
                ha="center",
                fontsize=10,
                fontweight="medium",
            )
        ax.set_xticks(x_pos)
        ax.set_xticklabels(
            [f"▸ {label}" for label in labels],
            color="#CBD5E1",
            fontsize=11,
            rotation=45,
            ha="right",
        )
        ax.tick_params(axis="y", which="both", length=0)
        plt.yticks(color="#64748B")
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color("#334155")
        card_text = (
            f"┌──────────────────────────────┐\n"
            f"│  📅 {datetime.now().strftime('%d %b %Y')}          │\n"
            f"├──────────────────────────────┤\n"
            f"│  ◉ Umumiy: {format_amount(total).rjust(12)}        |\n"
            f"│  ◎ O'rtacha: {format_amount(avg).rjust(10)}        |\n"
            f"│  ⚫ Ko'p sarf: {top_category[:15].ljust(12)}       |\n"
            f"└──────────────────────────────┘"
        )
        plt.text(
            0.72,
            0.88,
            card_text,
            transform=fig.transFigure,
            color="#CBD5E1",
            fontsize=12,
            bbox=dict(
                facecolor="#1E293B",
                edgecolor="#334155",
                boxstyle="round,pad=0.6",
                alpha=0.9,
            ),
        )
        plt.text(
            0.1,
            0.95,
            "Xarajatlar Analitikasi",
            transform=fig.transFigure,
            color="#E2E8F0",
            fontsize=20,
            fontweight="bold",
        )
        ax.yaxis.grid(True, color="#1E293B", linestyle="--", linewidth=0.8)
        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
        buffer.seek(0)
        plt.close()
        chart_file = BufferedInputFile(
            buffer.getvalue(), filename="expense_dashboard.png"
        )
        await message.answer_photo(
            photo=chart_file,
            caption=f"📊 Real-time xarajatlar monitoringi | {datetime.now().strftime('%d.%m.%Y')}",
        )
    except Exception as e:
        print(f"Error generating statistics: {str(e)}")
        await message.answer(
            "📛 Statistika yaratishda xatolik. Iltimos qayta urinib ko'ring!"
        )


@router.message(F.text == "🌟 Analitikani ko'rish (Jadval ko'rinishida)")
async def RequestPremium(message: Message):
    await message.answer(
        "🌟 Bu xususiyat faqat premium foydalanuvchilari uchun\n\n🔓 Premiumga ega bo'lish uchun @otabek_abdiraimov'ga yozing\n\n💰 Premium narxi 10.000 so'm."
    )
