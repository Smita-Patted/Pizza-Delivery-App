from fastapi import APIRouter,Depends,HTTPException,status
from schemas import OrderModel,OrderStatusModel
from models import User,Order
from db.database import Session,engine
import utils.oauth2 as oauth2
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(prefix='/order',tags=["Order"])

session = Session(bind = engine)


@order_router.post("/placeorder")
async def place_order(request:OrderModel,current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    print(f" current user {current_user}")
    new_order = Order(
        quantity = request.quantity,
        pizza_size = request.pizza_size,
        user_id = user.id
    )
    new_order.user = user
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    response = {
        "Pizza Quantity":new_order.quantity,
        "Pizza Size": new_order.pizza_size,
        "Order Id": new_order.id,
        "Order Status": new_order.order_status
    }
    return jsonable_encoder(response)


@order_router.get("/allorders")
def show_all_orders(current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You do not have permissions to view all orders")


@order_router.get("/myorders")
def show_myorders(current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()

    if user:
        orders = session.query(Order).filter(Order.user_id == user.id).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found")


@order_router.get("/vieworder/{order_id}")
def view_order_by_id(order_id,current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        orders = session.query(Order).filter(Order.id == order_id).first()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You do not have permissions to view orders")


@order_router.post("/update/{order_id}")
def update_orders(request:OrderModel, order_id,current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()
    if user:
        order = session.query(Order).filter(Order.id == order_id).first()
        order.quantity = request.quantity
        order.pizza_size = request.pizza_size
        session.commit()
        response ={
            "Updated Quantity":request.quantity,
            "Updated pizza size":request.pizza_size,
            "Updated Order's Id":order_id
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Order with Id doesn't exist")




@order_router.patch("/status/update/{order_id}")
def update_status(request:OrderStatusModel,order_id,current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()
        order.order_status = request.order_status
        session.commit()
        response = {
            "Status Updated to":request.order_status
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You are not a super user")



@order_router.delete("/delete/{order_id}")
def delete_orders(order_id,current_user: User = Depends(oauth2.get_current_user)):
    user = session.query(User).filter(User.username == current_user.username).first()

    if user:
        order = session.query(Order).filter(Order.id == order_id)
        order.delete(synchronize_session=False)
       
        session.commit()
        response = {
            "Order deleted": order_id
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You are not a super user")
