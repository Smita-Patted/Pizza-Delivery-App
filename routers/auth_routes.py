from fastapi import APIRouter,HTTPException,status
from werkzeug.security import generate_password_hash , check_password_hash
from schemas import SignUpModel,LoginModel
from models import User
from db.database import Session,engine
import utils.JWTtoken as JWTtoken


auth_router = APIRouter(prefix="/auth" ,tags=["Authentication"] )
session=Session(bind=engine)



@auth_router.post("/signup")
async def signup(request : SignUpModel):
    db_email = session.query(User).filter(User.email == request.email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email already exists") 

    db_username = session.query(User).filter(User.username == request.username).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with username already exists")
    
    new_user = User(
        username = request.username,
        email = request.email,
        password = generate_password_hash(request.password),
        is_active = request.is_active,
        is_staff = request.is_staff
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@auth_router.post("/login")
async def login(request: LoginModel):
    db_user = session.query(User).filter(User.username == request.username).first()

    if db_user and check_password_hash(db_user.password,request.password):

        access_token = JWTtoken.create_access_token(data={"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Token")