from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton

from bot.buttons.inline import build_inline_buttons
from bot.buttons.reply import reply_button_builder
from bot.functions import get_category, save_user
from db.model import Order, StatusEnum

main = Router()


@main.message(F.text == '◀️ Main Back')
@main.message(CommandStart())
async def start_handler(message: Message):
    user = {
        'user_id': message.from_user.id,
        'username': message.from_user.username,
    }
    await save_user(**user)
    buttons = ['🚚 Delivery services', '👤 Admin', '🧺 Basket']
    markup = await reply_button_builder(buttons, [2] * (len(buttons) // 2))
    await message.answer(text='✅ Welcome Delivery services bot:', reply_markup=markup)


@main.message(F.text == '🚚 Delivery services')
async def main_handler(message: Message):
    category = await  get_category()
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'category_{i.id}') for i in category]
    markup = await build_inline_buttons(buttons, [3] * (len(buttons) // 2))
    await message.answer(text='✅ Chose one service:', reply_markup=markup)


@main.message(F.text == '🧺 Basket')
async def card_handler(message: Message):
    user_id = message.chat.id
    orders: list[Order] = await Order.gets(Order.user_id, user_id)
    for order in orders:
        text = (
            f"🛍 <b>Name:</b> {order.product.name}\n"
            f"💵 <b>Price:</b> {order.product.price}\n"
            f"🚚 <b>Delivery:</b> {order.product.delivery_price}\n"
            f"💵 <b>Total Price:</b> {order.total_price}\n"
        )
        if order.status == StatusEnum.DELIVERY:
            address = order.address[0]
            await message.answer_location(latitude=address.latitude, longitude=address.longitude)
        await message.answer(text=text)


@main.message(F.text == '👤 Admin')
async def admin_handler(message: Message):
    await message.answer(text=f'https://t.me/Gorinhas')
