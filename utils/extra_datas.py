from decimal import Decimal

escape_chars = [
    "_",
    "*",
    "[",
    "]",
    "(",
    ")",
    "~",
    "`",
    ">",
    "#",
    "+",
    "-",
    "=",
    "|",
    "{",
    "}",
    ".",
    "!",
]


def make_title(title):
    name = ""
    for letter in title:
        if letter in escape_chars:
            name += f"\{letter}"
        else:
            name += letter
    return name


def format_amount(amount: Decimal) -> str:
    amount_float = float(amount)

    formatted_amount = f"{amount:,.0f}".replace(",", " ")

    if amount_float.is_integer():
        formatted_amount = formatted_amount.split(".")[0]

    return formatted_amount
