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
    order = relationship('Order', back_populates='user')

class Category(CreatedModel):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String)
    product = relationship('Product', back_populates='category')
    service = relationship('Service', back_populates='category')

    def __repr__(self):
        return f"{self.name}"


class Product(CreatedModel):
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(Text)
    count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id', ondelete='CASCADE'))
    category = relationship('Category', back_populates='product')
    service = relationship('Service', back_populates='product')
    order = relationship('Order', back_populates='product')

    def __repr__(self):
        return f"{self.name},{self.price},{self.image},{self.category_id},{self.count}"


class Order(CreatedModel):
    product_name: Mapped[str] = mapped_column(String)
    product_price: Mapped[int] = mapped_column(Float)
    delivery: Mapped[int] = mapped_column(Integer, default=20000)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    product = relationship('Product', back_populates='order')
    user = relationship('User', back_populates='order')
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
    category = relationship('Category', back_populates='service')
    product = relationship('Product', back_populates='service')

    def __repr__(self):
        return f"{self.name}"


class Address(CreatedModel):
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.latitude},{self.longitude}'
metadata = Base.metadata
