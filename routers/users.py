from fastapi import  Depends, HTTPException, Path, APIRouter, Request, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from models import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext
router=APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db=SessionLocal()
    try:
        yield  db
    finally:
        db.close()

db_dependency=  Annotated[Session,Depends(get_db)]
user_dependency= Annotated[dict,Depends(get_current_user)]
bcrypt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory="templates")

class UserVerification(BaseModel):
    username: str
    password:str
    new_password:str=Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put('/edit-password', response_class=HTMLResponse)
async def edit_user_view(user:user_dependency,
                            db:db_dependency,
                            user_verification:UserVerification):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("edit-password.html", {
        "request": user_verification,
        "user": user,
    })

@router.post("/edit-password",response_class=HTMLResponse)
async def user_password_change(request:Request, db:db_dependency,user:user_dependency,
                               username:str=Form(...),password:str=Form(...),
                               password2:str=Form(...)):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    user_data= db.query(Users).filter(Users.username==user.get('username')).first()
    msg="Invalid username or password"

    if user_data is not None:
        if username==user_data.username and bcrypt_context.verify(password, user_data.hashed_password):
            user_data.password=bcrypt_context.hash(password2)
            db.add(user_data)
            db.commit()
            msg="Password updated"
    return templates.TemplateResponse("edit-password.html", {"request": request, "user": user, "msg": msg})


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency,db:db_dependency,
                              phone_number:str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()