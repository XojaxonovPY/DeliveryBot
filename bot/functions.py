from db.model import Category, Service, Product, User, Order, Address


async def save_user(**kwargs):
    check = await User.get(User.user_id, kwargs.get('user_id'))
    if not check:
        await User.create(**kwargs)


async def get_category():
    category: list[Category] = await Category.get_all()
    return category


async def get_service(category_id: str):
    id_ = ''.join([i for i in category_id if i.isdigit()])
    service: list[Service] = await Service.get(Service.category_id, int(id_))
    return service


async def get_product(service_id: str):
    id_ = ''.join([i for i in service_id if i.isdigit()])
    product: list[Product] = await Product.get(Product.service_id, int(id_))
    return product


async def product_check(product_id, quantity):
    count = await Product.gets(Product.id, product_id, Product.count)
    name = await Product.gets(Product.id, product_id, Product.name)
    price = await Product.gets(Product.id, product_id, Product.price)
    if not quantity.isdigit():
        return '❌', 'Please enter how much you want to pay.', f'({quantity}) is error'
    if count[0] < int(quantity):
        return "❌", "We don't have that many.", f'({count[0]})maximal take'
    return quantity, name[0], price[0]


async def get_cards(user_id):
    address: list[Address] = await Address.get(Address.user_id, user_id)
    items = '|'.join(await Order.gets(Order.user_id, user_id, Order.product_name))
    price = await Order.gets(Order.user_id, user_id, Order.product_price)
    count = await Order.gets(Order.user_id, user_id, Order.quantity)
    status_list = await Order.gets(Order.user_id, user_id, Order.status)
    status = '|'.join(s.value for s in status_list)
    total_price = 0
    total_count = 0
    for p, c in zip(price, count):
        total_price += p
        total_count += c
    return items, total_price, total_count, address, status


async def check_address(user_id):
    query = await Address.get(Address.user_id, user_id)
    if query:
        return False
    return True
