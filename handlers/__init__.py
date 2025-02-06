from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import (
        admin,
        start,
        help,
        expense,
        income,
        see_all_expenses,
        see_all_incomes,
        see_general_stats,
    )
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

    router.include_routers(
        admin.router,
        start.router,
        help.router,
        expense.router,
        income.router,
        see_all_incomes.router,
        see_all_expenses.router,
        see_general_stats.router,
        error_handler.router,
    )

    return router
