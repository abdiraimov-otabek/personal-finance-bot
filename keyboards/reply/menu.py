from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menukey = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌟 Analitikani ko'rish (Jadval ko'rinishida)")],
        [
            KeyboardButton(text="💰 Xarajat kiritish"),
            KeyboardButton(text="📥 Daromad kiritish"),
        ],
        [
            KeyboardButton(text="📊 Xarajatlarni ko‘rish"),
            KeyboardButton(text="📈 Daromadlarni ko‘rish"),
        ],
        [KeyboardButton(text="💡 Umumiy statistikani ko‘rish")],
    ],
    resize_keyboard=True,
)
