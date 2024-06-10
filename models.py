from db.database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    username = Column(String(20),unique=True)
    email = Column(String(50),unique=True)
    password = Column(Text,nullable=False)
    is_staff=Column(Boolean,default=False)
    is_active = Column(Boolean,default=False)
    orders = relationship('Order',back_populates='user')

    def __repr__(self):
        return f"Username : {self.username}"
    

class Order(Base):
    __tablename__ = 'orders'

    ORDER_STATUSES = (
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered')
    )

    PIZZA_SIZES = (
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA LARGE','extra large')
    )

    id = Column(Integer,primary_key=True)
    quantity = Column(Integer,nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES),default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES),default='small')
    user_id = Column(Integer,ForeignKey('users.id'))

    user = relationship('User',back_populates="orders")

    def __repr__(self):
        return f"Order : {self.id}"