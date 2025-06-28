from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.buttons.inline import build_inline_buttons
from bot.buttons.reply import reply_button_builder
from db.model import Address, Order, Service, Product, StatusEnum

deliver = Router()


@deliver.callback_query(F.data.startswith('category_'))
async def category_handler(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    service: list[Service] = await Service.gets(Service.category_id, category_id)
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'service_{i.id}') for i in service]
    markup = await build_inline_buttons(buttons, [2] * (len(service) // 2))
    await callback.message.answer(text='✅ Which service:', reply_markup=markup)


@deliver.callback_query(F.data.startswith('service_'))
async def service_handler(callback: CallbackQuery):
    service_id = int(callback.data.split('_')[1])
    product: list[Product] = await Product.gets(Product.service_id, service_id)
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'product_{i.id}') for i in product]
    markup = await build_inline_buttons(buttons, [2] * (len(buttons) // 2))
    await callback.message.answer(text='✅ Chose product:', reply_markup=markup)


@deliver.callback_query(F.data.startswith('product_'))
async def product_handler(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split('_')[1])
    product: Product = await Product.get(Product.id, product_id)
    await state.update_data(product=product)
    text = (
            f"🛍 <b>Name:</b> {product.name}\n"
            f"💵 <b>Price:</b> {product.price}\n"
            f"🚚 <b>Delivery:</b> {product.delivery_price}\n"
        )
    button = [InlineKeyboardButton(text='✅ Ordered', callback_data='ordered')]
    markup = await build_inline_buttons(button, [1])
    await callback.message.answer(text=text, reply_markup=markup)


@deliver.callback_query(F.data=='ordered')
async def product_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product: Product = data.get('product')
    user_id = callback.message.chat.id
    num = callback.message.text
    item = {
        'product_id': product.id,
        'quantity': product.count,
        'user_id': user_id,
        'total_price': product.price + product.delivery_price
    }
    order = await Order.create(**item)
    await state.clear()
    await state.update_data(order=order)
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text='🛒 Check out', request_location=True),KeyboardButton(text='◀️ Main Back'))
    rkb.adjust(2)
    rkb = rkb.as_markup(resize_keyboard=True)
    await callback.message.answer('✅ Added to cart', reply_markup=rkb)


@deliver.message(F.location)
async def location_handler(message: Message,state:FSMContext):
    data = await state.get_data()
    order:Order = data.get('order')
    await Order.update(Order.id,order.id,status=StatusEnum.DELIVERY)
    location = message.location
    lock = {
        'latitude': location.latitude,
        'longitude': location.longitude,
        'order_id': order.id
    }
    markup = reply_button_builder(['◀️ Main Back'])
    await Address.create(**lock)
    await message.answer('✅ Your location find order is go')
