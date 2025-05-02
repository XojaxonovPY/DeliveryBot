from aiogram.utils.keyboard import InlineKeyboardBuilder


async def build_inline_buttons(buttons , size=(1,)):
    rkb = InlineKeyboardBuilder()
    rkb.add(*buttons)
    rkb.adjust(*size)
    return rkb.as_markup()