from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException

#local imports
from .models import Users, UserInformations
from .schemas import UserBase, UserFullData, UserInfos

# from main import JWT_SECRET
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

def get_all_users(db:Session):
    users = db.query(Users).all()
    # user_infos = db.query(UserInformations).all()
    return users


def create_user(db:Session, user:UserFullData):
    user_obj = Users(email=user.email, name=user.name)
    user_obj.password = bcrypt.hash(user.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    ui = user.user_informations
    user_info = UserInformations(address=ui.address, phone=ui.phone, dob=ui.dob, user_id=user_obj.id)
    db.add(user_info)
    db.commit()
    db.refresh(user_info)
    user.id, user.user_informations.id = user_obj.id, user_info.id
    return user

def authorize_user(db:Session, email:str, password:str):
    user = db.query(Users).filter(Users.email==email).first()
    if user:
        if bcrypt.verify(password, user.password):
            user = {
                "id":user.id,
                "email": user.email,
                "password": user.password,
                "name":user.name
            }
            return user  
        else:
            return HTTPException(status_code=401, detail="UnAuthorized")
    else:
        return HTTPException(status_code=403, detail="Invalid credentials")



def get_cur_user_infos(db:Session, token:str):
    data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    try:
        user = db.query(Users).filter(Users.email==data['email']).first()
        if user.password == data['password']:
            user_info = user.user_informations[0]
            ui = {
                'address': user_info.address,
                'phone': user_info.phone,
                'dob': user_info.dob}
            user_data = {
                "id":user.id, 
                "email":user.email, 
                "name": user.name,
                "password":user.password, 
                "user_informations":ui 
            }
            
            # print(ui)
            # user_data.update({''})
            return user_data
    except:
        return HTTPException(status_code=400, detail="Token has been corrupted.")