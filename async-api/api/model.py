from sqlalchemy import Integer, String, Numeric, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    products = relationship(
        'Product',
        secondary='UserProductLikes',
        back_populates='users'
    )


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    price = Column(Numeric)
    description = Column(String)

    users = relationship(
        'User',
        secondary='UserProductLikes',
        back_populates='products'
    )


class UserProductLikes(Base):
    __tablename__ = 'user_product_likes'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
