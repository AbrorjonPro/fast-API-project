from datetime import date
from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    id: Optional[int]
    email: str
    password: str
    name: str

    class Config:
        orm_mode = True


class UserInfos(BaseModel):
    id: Optional[int]
    address: str
    phone: str
    dob: date

    class Config:
        orm_mode = True

class UserFullData(UserBase):
    user_informations: UserInfos


class UserAllData(UserBase):
    user_informations: List[UserInfos] = None
    
    