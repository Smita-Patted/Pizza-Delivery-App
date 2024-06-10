from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from routers.auth_routes import auth_router
from routers.order_routes import order_router
from fastapi import FastAPI


app = FastAPI()
 
# Configure templates
templates = Jinja2Templates(directory="templates")
 
@app.get("/", response_class=HTMLResponse, tags=["Default"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(auth_router)
app.include_router(order_router)