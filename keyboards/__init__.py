from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import get_text

CATEGORIES = ["food", "transport", "shopping", "entertainment", "education", "health", "bills", "other"]


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "add_expense"), callback_data="add_expense")],
        [InlineKeyboardButton(text=get_text(lang, "add_income"), callback_data="add_income")],
        [InlineKeyboardButton(text=get_text(lang, "statistics"), callback_data="statistics")],
        [InlineKeyboardButton(text=get_text(lang, "history"), callback_data="history")],
        [InlineKeyboardButton(text=get_text(lang, "settings"), callback_data="settings")],
    ])


def categories_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for cat in CATEGORIES:
        label = get_text(lang, f"categories.{cat}")
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"category:{cat}")])
    buttons.append([InlineKeyboardButton(text=get_text(lang, "cancel"), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def skip_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "skip"), callback_data="skip_description")],
        [InlineKeyboardButton(text=get_text(lang, "cancel"), callback_data="main_menu")],
    ])


def back_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="main_menu")],
    ])


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
    ])


def history_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "expenses_list"), callback_data="view_expenses")],
        [InlineKeyboardButton(text=get_text(lang, "incomes_list"), callback_data="view_incomes")],
        [InlineKeyboardButton(text=get_text(lang, "last_transactions"), callback_data="last_transactions")],
        [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="main_menu")],
    ])


def statistics_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "monthly_summary"), callback_data="monthly_summary")],
        [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="main_menu")],
    ])


def settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "change_language"), callback_data="change_language")],
        [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="main_menu")],
    ])


def expense_list_keyboard(lang: str, expenses: list) -> InlineKeyboardMarkup:
    buttons = []
    for expense in expenses:
        label = f"🗑 #{expense.id} | {expense.amount:.2f} | {expense.category} | {expense.date.strftime('%d.%m')}"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"del_expense:{expense.id}")])
    buttons.append([InlineKeyboardButton(text=get_text(lang, "back"), callback_data="history")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def income_list_keyboard(lang: str, incomes: list) -> InlineKeyboardMarkup:
    buttons = []
    for income in incomes:
        label = f"🗑 #{income.id} | {income.amount:.2f} | {income.date.strftime('%d.%m')}"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"del_income:{income.id}")])
    buttons.append([InlineKeyboardButton(text=get_text(lang, "back"), callback_data="history")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_delete_keyboard(lang: str, record_type: str, record_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "yes_delete"), callback_data=f"confirm_del_{record_type}:{record_id}")],
        [InlineKeyboardButton(text=get_text(lang, "no_cancel"), callback_data="history")],
    ])
