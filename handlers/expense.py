from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.states import AddExpenseState
from services import get_language, add_expense, get_expenses, delete_expense
from keyboards import categories_keyboard, skip_keyboard, back_keyboard, expense_list_keyboard, confirm_delete_keyboard
from localization import get_text

router = Router()


@router.callback_query(lambda c: c.data == "add_expense")
async def start_add_expense(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)
    await state.set_state(AddExpenseState.choosing_category)
    await callback.message.edit_text(
        get_text(lang, "choose_category"),
        reply_markup=categories_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("category:"), AddExpenseState.choosing_category)
async def choose_category(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)
    category = callback.data.split(":")[1]
    await state.update_data(category=category)
    await state.set_state(AddExpenseState.entering_amount)
    await callback.message.edit_text(
        get_text(lang, "enter_amount"),
        reply_markup=back_keyboard(lang),
    )
    await callback.answer()


@router.message(AddExpenseState.entering_amount)
async def enter_amount(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer(get_text(lang, "invalid_amount"))
        return

    await state.update_data(amount=amount)
    await state.set_state(AddExpenseState.entering_description)
    await message.answer(
        get_text(lang, "enter_description"),
        reply_markup=skip_keyboard(lang),
    )


@router.message(AddExpenseState.entering_description)
async def enter_description(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    data = await state.get_data()
    add_expense(message.from_user.id, data["amount"], data["category"], message.text)
    await state.clear()
    await message.answer(
        get_text(lang, "expense_added"),
        reply_markup=back_keyboard(lang),
    )


@router.callback_query(lambda c: c.data == "skip_description", AddExpenseState.entering_description)
async def skip_description_expense(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)
    data = await state.get_data()
    add_expense(callback.from_user.id, data["amount"], data["category"])
    await state.clear()
    await callback.message.edit_text(
        get_text(lang, "expense_added"),
        reply_markup=back_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "view_expenses")
async def view_expenses(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    expenses = get_expenses(callback.from_user.id, limit=20)
    if not expenses:
        await callback.message.edit_text(
            get_text(lang, "no_expenses"),
            reply_markup=back_keyboard(lang),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        get_text(lang, "expenses_list"),
        reply_markup=expense_list_keyboard(lang, expenses),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("del_expense:"))
async def confirm_delete_expense(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    expense_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        get_text(lang, "confirm_delete"),
        reply_markup=confirm_delete_keyboard(lang, "expense", expense_id),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_del_expense:"))
async def do_delete_expense(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    expense_id = int(callback.data.split(":")[1])
    delete_expense(expense_id, callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "expense_deleted"),
        reply_markup=back_keyboard(lang),
    )
    await callback.answer()
