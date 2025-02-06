from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard = [
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="yes"),
        InlineKeyboardButton(text="❌ No", callback_data="no"),
    ]
]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

inline_keyboard = [
    [
        InlineKeyboardButton(text="✅ Ha", callback_data="yes"),
        InlineKeyboardButton(text="❌ Tahrirlash", callback_data="no"),
    ]
]
choise_data = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

inline_keyboard = [
    [
        InlineKeyboardButton(
            text="📄 Hisobotni yuklab olish", callback_data="get_excel_file"
        )
    ],
]

download_data = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

inline_keyboard = [
    [
        InlineKeyboardButton(text="🏠 Uy-joy", callback_data="expense_uy-joy"),
        InlineKeyboardButton(text="🍽️ Yegulik", callback_data="expense_yegulik"),
    ],
    [
        InlineKeyboardButton(text="🚗 Transport", callback_data="expense_transport"),
        InlineKeyboardButton(text="🛒 Xaridlar", callback_data="expense_xaridlar"),
    ],
    [
        InlineKeyboardButton(text="🎮 O'yinlar", callback_data="expense_o'yinlar"),
        InlineKeyboardButton(
            text="💡 Kommunal to'lovlar", callback_data="expense_kommunal-to'lovlar"
        ),
    ],
    [
        InlineKeyboardButton(text="📱 Telefon", callback_data="expense_telefon"),
        InlineKeyboardButton(
            text="💼 Ishlab chiqarish", callback_data="expense_ishlab-chiqarish"
        ),
    ],
    [
        InlineKeyboardButton(text="🎁 Sovg'alar", callback_data="expense_sovg'alar"),
        InlineKeyboardButton(
            text="💊 Dori-darmon", callback_data="expense_dori-darmon"
        ),
    ],
    [
        InlineKeyboardButton(text="🏖️ Sayohat", callback_data="expense_sayohat"),
        InlineKeyboardButton(text="📚 Ta'lim", callback_data="expense_ta'lim"),
    ],
    [
        InlineKeyboardButton(text="🏋️‍♂️ Sport", callback_data="expense_sport"),
        InlineKeyboardButton(text="💼 Karyera", callback_data="expense_karyera"),
    ],
    [
        InlineKeyboardButton(text="🛠️ Ta'mirlash", callback_data="expense_ta'mirlash"),
        InlineKeyboardButton(text="💳 Boshqa", callback_data="expense_boshqa"),
    ],
]

expense_categories = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

inline_keyboard = [
    [
        InlineKeyboardButton(text="💼 Maosh", callback_data="income_salary"),
        InlineKeyboardButton(text="💵 Nafaqa", callback_data="income_allowance"),
    ],
    [
        InlineKeyboardButton(text="🎁 Bonuslar", callback_data="income_bonus"),
    ],
    [
        InlineKeyboardButton(text="💸 Boshqa", callback_data="income_other"),
    ],
]

income_categories = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
