from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.buttons.inline import build_inline_buttons
from bot.functions import get_service, get_product, product_check, check_address
from bot.states import States
from db.model import Address, Order

deliver = Router()


@deliver.callback_query(F.data.startswith('category'))
async def category_handler(callback: CallbackQuery):
    category_id = callback.data
    service = await get_service(category_id)
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'service_{i.id}') for i in service]
    markup = await build_inline_buttons(buttons, [2] * (len(service) // 2))
    await callback.message.answer(text='✅ Which service:', reply_markup=markup)


@deliver.callback_query(F.data.startswith('service'))
async def service_handler(callback: CallbackQuery):
    service_id = callback.data
    product = await get_product(service_id)
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'product_{i.id}') for i in product]
    markup = await build_inline_buttons(buttons, [2] * (len(buttons) // 2))
    await callback.message.answer(text='✅ Chose product:', reply_markup=markup)


@deliver.callback_query(F.data.startswith('product'))
async def product_handler(callback: CallbackQuery, state: FSMContext):
    call = callback.data
    product_id = int(''.join([i for i in call if i.isdigit()]))
    await state.update_data(product_id=product_id)
    await state.set_state(States.quantity)
    await callback.message.answer(text='✅ How much:')


@deliver.message(States.quantity)
async def quantity_handler(message: Message, state: FSMContext):
    user_id = message.chat.id
    num = message.text
    data = await state.get_data()
    product_id = data.get('product_id')
    quantity, name, price = await product_check(product_id, num)
    if quantity == '❌':
        await message.answer(text=quantity + name + price)
    item = {
        'product_id': product_id,
        'quantity': int(quantity),
        'product_name': name,
        'product_price': price,
        'user_id': user_id
    }
    await Order.create(**item)
    await state.clear()
    rkb = ReplyKeyboardBuilder()
    query = await check_address(user_id)
    if query:
        rkb.add(KeyboardButton(text='🛒 Check out', request_location=True))
    rkb.add(KeyboardButton(text='◀️ Main Back'))
    rkb.adjust(1)
    rkb = rkb.as_markup(resize_keyboard=True)
    await message.answer('✅ Added to cart', reply_markup=rkb)


@deliver.message(F.location)
async def location_handler(message: Message):
    user_id = message.chat.id
    location = message.location
    lock = {
        'latitude': location.latitude,
        'longitude': location.longitude,
        'user_id': user_id
    }
    await Address.create(**lock)
    await message.answer('✅ Your location find order is go')
