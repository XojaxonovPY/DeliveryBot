from sqlalchemy import Text, String, BIGINT, ForeignKey, Integer, Float, Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base, db
from db.utils import CreatedModel
import enum


class StatusEnum(enum.Enum):
    ACCEPTED = "accepted"
    DELIVERY = "delivery"
    DELIVERED = "delivered"


class User(CreatedModel):
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    order = relationship('Order', back_populates='user',lazy='selectin')

class Category(CreatedModel):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String)
    service = relationship('Service', back_populates='category',lazy='selectin')

    def __repr__(self):
        return f"{self.name}"


class Product(CreatedModel):
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(Text)
    count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id', ondelete='CASCADE'))
    delivery_price: Mapped[float] = mapped_column(Float,nullable=True)
    service = relationship('Service', back_populates='product',lazy='selectin')
    order = relationship('Order', back_populates='product',lazy='selectin')

    def __repr__(self):
        return f"{self.name},{self.price},{self.image},{self.service_id},{self.count}"


class Order(CreatedModel):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Float,nullable=True)
    product = relationship('Product', back_populates='order',lazy='selectin')
    user = relationship('User', back_populates='order',lazy='selectin')
    address=relationship('Address',back_populates='order',lazy='selectin')
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name="status_enum", create_constraint=True),
        default=StatusEnum.ACCEPTED,
        nullable=False
    )

    def __repr__(self):
        return f'{self.quantity},{self.user_id},{self.product_id}'

    @classmethod
    async def create_all(cls, s: str, n: str):
        objs = []
        for name in s.split():
            obj = cls(**{n: name})
            objs.append(obj)
        db.add_all(objs)
        await db.commit()
        return objs


class Service(CreatedModel):
    name: Mapped[str] = mapped_column(String())
    category_id = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category = relationship('Category', back_populates='service',lazy='selectin')
    product = relationship('Product', back_populates='service',lazy='selectin')

    def __repr__(self):
        return f"{self.name}"


class Address(CreatedModel):
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    order = relationship('Order', back_populates='address',lazy='selectin')

    def __repr__(self):
        return f'{self.latitude},{self.longitude}'
metadata = Base.metadata
