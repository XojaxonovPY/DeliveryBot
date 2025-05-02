from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from bot.buttons.reply import reply_button_builder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from bot.states import States

language=Router()


@language.message(F.text == __('🇷🇺 🇺🇿 Tillar'))
async def language_user(message: Message, state: FSMContext):
    text = ['🇺🇿 Uzb','🇷🇺 Rus', _('◀️ Orqaga')]
    markup = await reply_button_builder(text, (3, 1))
    await state.set_state(States.lang)
    await message.answer(text=_('Tilni tanlang:'), reply_markup=markup)


@language.message(States.lang)
async def language_handler(message: Message, state: FSMContext, i18n):
    map_lang = {
        '🇺🇿 Uzb': 'uz',
        '🇷🇺 Rus': 'ru'
    }
    code = map_lang.get(message.text)
    i18n.current_locale = code
    lang = await state.get_value('locale')
    await state.clear()
    await state.update_data({'locale': lang})
    await state.update_data(locale=code)
    text = [_('🏬 Mahsulotlar bolimi'), _('📦 Haridlar'), _('🇷🇺 🇺🇿 Tillar'), _('📞 Aloqa')]
    markup = await reply_button_builder(text, (3, 1))
    await message.answer(text=_('✅ Hush kelibsiz!'), reply_markup=markup)