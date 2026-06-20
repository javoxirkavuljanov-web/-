from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from services import get_or_create_user, set_language, get_language
from keyboards import main_menu_keyboard, language_keyboard, settings_keyboard
from localization import get_text

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    get_or_create_user(message.from_user.id, message.from_user.username)
    await message.answer(
        get_text("en", "welcome"),
        reply_markup=language_keyboard(),
    )


@router.callback_query(lambda c: c.data.startswith("lang:"))
async def set_lang(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    set_language(callback.from_user.id, lang)
    await callback.message.edit_text(
        get_text(lang, "language_set"),
    )
    await callback.message.answer(
        get_text(lang, "main_menu"),
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "main_menu"),
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "settings")
async def settings(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "settings_menu"),
        reply_markup=settings_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "change_language")
async def change_language(callback: CallbackQuery):
    await callback.message.edit_text(
        get_text("en", "welcome"),
        reply_markup=language_keyboard(),
    )
    await callback.answer()
