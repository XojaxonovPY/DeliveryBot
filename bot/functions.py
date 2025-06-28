from db.model import Category, Service, Product, User, Order, Address


async def save_user(**kwargs):
    check = await User.get(User.user_id, kwargs.get('user_id'))
    if not check:
        await User.create(**kwargs)


