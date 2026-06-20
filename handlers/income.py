from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.states import AddIncomeState
from services import get_language, add_income, get_incomes, delete_income
from keyboards import skip_keyboard, back_keyboard, income_list_keyboard, confirm_delete_keyboard
from localization import get_text

router = Router()


@router.callback_query(lambda c: c.data == "add_income")
async def start_add_income(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)
    await state.set_state(AddIncomeState.entering_amount)
    await callback.message.edit_text(
        get_text(lang, "enter_amount"),
        reply_markup=back_keyboard(lang),
    )
    await callback.answer()


@router.message(AddIncomeState.entering_amount)
async def enter_amount(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer(get_text(lang, "invalid_amount"))
        return

    await state.update_data(amount=amount)
    await state.set_state(AddIncomeState.entering_description)
    await message.answer(
        get_text(lang, "enter_description"),
        reply_markup=skip_keyboard(lang),
    )


@router.message(AddIncomeState.entering_description)
async def enter_description(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    data = await state.get_data()
    add_income(message.from_user.id, data["amount"], message.text)
    await state.clear()
    await message.answer(
        get_text(lang, "income_added"),
        reply_markup=back_keyboard(lang),
    )


@router.callback_query(lambda c: c.data == "skip_description", AddIncomeState.entering_description)
async def skip_description_income(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)
    data = await state.get_data()
    add_income(callback.from_user.id, data["amount"])
    await state.clear()
    await callback.message.edit_text(
        get_text(lang, "income_added"),
        reply_markup=back_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "view_incomes")
async def view_incomes(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    incomes = get_incomes(callback.from_user.id, limit=20)
    if not incomes:
        await callback.message.edit_text(
            get_text(lang, "no_incomes"),
            reply_markup=back_keyboard(lang),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        get_text(lang, "incomes_list"),
        reply_markup=income_list_keyboard(lang, incomes),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("del_income:"))
async def confirm_delete_income(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    income_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        get_text(lang, "confirm_delete"),
        reply_markup=confirm_delete_keyboard(lang, "income", income_id),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_del_income:"))
async def do_delete_income(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    income_id = int(callback.data.split(":")[1])
    delete_income(income_id, callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "income_deleted"),
        reply_markup=back_keyboard(lang),
    )
    await callback.answer()
