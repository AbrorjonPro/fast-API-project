from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
import jwt
#local imports
from db.database import SessionLocal
from db.crud import *
from db.sql_queries import get_user_infos
from db.schemas import UserAllData, UserFullData
app = FastAPI(
    title="FAST API BY Abror",
    #version="0.0.1",
)
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/v1/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/v1/token")
async def token(form:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user= authorize_user(db, form.username, form.password)

    if user and type(user)==dict:
        token = jwt.encode(user, JWT_SECRET)

        data = {
            "token":token,
            "type": "bearer"
        }
        return data
    return user

@app.post("/api/v1/users", response_model=UserFullData)
async def create_new_user(form:UserFullData, db:Session=Depends(get_db)):
    new_user = create_user(db, form)
    return new_user

@app.get("/api/v1/users")   #, response_model=List[UserAllData]
async def get_users(db:Session=Depends(get_db)):
    users = get_user_infos()
    return users

@app.get("/api/v1/users/{user_id}")   #, response_model=List[UserAllData]
async def get_users(user_id:int, db:Session=Depends(get_db)):
    users = get_user_infos()
    return users


@app.get("/api/v1/users/me/")
async def get_me(db:Session=Depends(get_db), token: str=Depends(oauth2_schema)):
    user_data = get_cur_user_infos(db, token)
    return user_data
