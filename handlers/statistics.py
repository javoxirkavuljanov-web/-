from datetime import datetime
from aiogram import Router
from aiogram.types import CallbackQuery
from services import get_language, get_total_expenses, get_total_income, get_expenses_by_month, get_incomes_by_month
from keyboards import statistics_keyboard, back_keyboard, history_keyboard
from localization import get_text

router = Router()


@router.callback_query(lambda c: c.data == "statistics")
async def statistics(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    total_income = get_total_income(callback.from_user.id)
    total_expenses = get_total_expenses(callback.from_user.id)
    balance = total_income - total_expenses

    balance_emoji = "✅" if balance >= 0 else "❌"

    text = (
        f"📊 <b>{get_text(lang, 'statistics_title')}</b>\n\n"
        f"💰 {get_text(lang, 'total_income')}: <b>{total_income:.2f}</b>\n"
        f"💸 {get_text(lang, 'total_expenses')}: <b>{total_expenses:.2f}</b>\n"
        f"{balance_emoji} {get_text(lang, 'balance')}: <b>{balance:.2f}</b>"
    )

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=statistics_keyboard(lang))
    await callback.answer()


@router.callback_query(lambda c: c.data == "monthly_summary")
async def monthly_summary(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    now = datetime.utcnow()
    year, month = now.year, now.month

    expenses = get_expenses_by_month(callback.from_user.id, year, month)
    incomes = get_incomes_by_month(callback.from_user.id, year, month)

    month_names = get_text(lang, "month_names")
    month_name = month_names[month - 1]

    total_exp = sum(e.amount for e in expenses)
    total_inc = sum(i.amount for i in incomes)
    balance = total_inc - total_exp

    category_totals: dict[str, float] = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    text = f"📅 <b>{get_text(lang, 'monthly_summary')} — {month_name} {year}</b>\n\n"
    text += f"💰 {get_text(lang, 'total_income')}: <b>{total_inc:.2f}</b>\n"
    text += f"💸 {get_text(lang, 'total_expenses')}: <b>{total_exp:.2f}</b>\n"

    balance_emoji = "✅" if balance >= 0 else "❌"
    text += f"{balance_emoji} {get_text(lang, 'balance')}: <b>{balance:.2f}</b>\n"

    if category_totals:
        text += "\n<b>By category:</b>\n"
        for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            cat_label = get_text(lang, f"categories.{cat}")
            text += f"  {cat_label}: {amount:.2f}\n"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_keyboard(lang))
    await callback.answer()


@router.callback_query(lambda c: c.data == "history")
async def history(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "history"),
        reply_markup=history_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "last_transactions")
async def last_transactions(callback: CallbackQuery):
    from services import get_expenses, get_incomes
    lang = get_language(callback.from_user.id)

    expenses = get_expenses(callback.from_user.id, limit=10)
    incomes = get_incomes(callback.from_user.id, limit=10)

    transactions = []
    for e in expenses:
        transactions.append(("expense", e.amount, e.category, e.description, e.date))
    for i in incomes:
        transactions.append(("income", i.amount, None, i.description, i.date))

    transactions.sort(key=lambda x: x[4], reverse=True)
    transactions = transactions[:10]

    if not transactions:
        await callback.message.edit_text(
            get_text(lang, "nothing_found"),
            reply_markup=back_keyboard(lang),
        )
        await callback.answer()
        return

    text = f"🕐 <b>{get_text(lang, 'last_transactions')}</b>\n\n"
    for t_type, amount, category, desc, date in transactions:
        date_str = date.strftime("%d.%m.%Y")
        if t_type == "expense":
            cat_label = get_text(lang, f"categories.{category}")
            label = get_text(lang, "expense_label")
            text += f"💸 {label} | {amount:.2f} | {cat_label}"
        else:
            label = get_text(lang, "income_label")
            text += f"💰 {label} | {amount:.2f}"
        if desc:
            text += f" | {desc}"
        text += f" | {date_str}\n"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_keyboard(lang))
    await callback.answer()
