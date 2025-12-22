from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


# Request Models
class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    profile_img: Optional[str] = None
    status: str = "active"


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_img: Optional[str] = None
    status: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


# Response Models
class UserResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    email: EmailStr
    phone: Optional[str] = None
    profile_img: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
