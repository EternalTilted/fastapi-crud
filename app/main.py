from fastapi import FastAPI, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import get_session, disconnect
from crud import get_users, create_user, get_user, delete_user, update_user
from schemas import UserCreate, UserUpdate
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    get_session()
    try:
        yield
    finally:
        await disconnect()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="static/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request, db: AsyncSession = Depends(get_session)):
    users = await get_users(db)
    return templates.TemplateResponse(request=request, name='index.html', context={"users": users})


@app.post("/create-user", response_class=HTMLResponse)
async def create_user_view(request: Request, db: AsyncSession = Depends(get_session),
                           first_name: str = Form(...),
                           last_name: str = Form(...),
                           email: str = Form(...)):
    user = UserCreate(first_name=first_name, last_name=last_name, email=email)
    await create_user(db, user)
    users = await get_users(db)
    return templates.TemplateResponse(request=request, name='table.html', context={"users": users})


@app.get("/edit_row/{id}", response_class=HTMLResponse)
async def update_user_view(id: int, request: Request, db: AsyncSession = Depends(get_session)):
    user = await get_user(db=db, user_id=id)
    print(id)
    print(user.id, user.first_name, user.last_name, user.email)
    return templates.TemplateResponse(request=request, name='edit_row.html', context={"user": user})


@app.post("/confirm-update/{id}", response_class=HTMLResponse)
async def confirm_update(id: int,
                         request: Request,
                         db: AsyncSession = Depends(get_session),
                         first_name: str = Form(...),
                         last_name: str = Form(...),
                         email: str = Form(...)
                         ):
    user = UserUpdate(id=id, first_name=first_name, last_name=last_name, email=email)
    await update_user(db=db, user=user)
    users = await get_users(db)
    return templates.TemplateResponse(request=request, name='table.html', context={"users": users})


@app.delete("/delete-user/{id}")
async def delete_user_view(id: int, request: Request, db: AsyncSession = Depends(get_session)):
    await delete_user(db, id)
    users = await get_users(db)
    return templates.TemplateResponse(request=request, name='table.html', context={"users": users})

