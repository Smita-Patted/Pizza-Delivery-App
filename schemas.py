from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = False

    class Config:
        from_attributes = True 
        

class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    quantity :int
    order_status : Optional[str] = "PENDING"
    pizza_size :Optional[str] = "SMALL"
  
    class Config:
        form_attribute = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class OrderStatusModel(BaseModel):
    order_status : Optional[str] = 'PENIDNG'

    class Config:
        form_attribute = True
