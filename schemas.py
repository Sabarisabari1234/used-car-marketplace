from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    phone: str = Field(min_length=10, max_length=15)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CarBase(BaseModel):
    brand: str = Field(min_length=2, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1990, le=2100)
    price: int = Field(gt=0)
    fuel_type: str = Field(min_length=3, max_length=20)
    transmission: str = Field(min_length=3, max_length=20)
    kilometers: int = Field(ge=0)
    owner_count: int = Field(ge=1, le=10)
    color: str = Field(min_length=3, max_length=30)
    city: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=1000)

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=2, max_length=50)
    model: str | None = Field(default=None, min_length=1, max_length=50)
    year: int | None = Field(default=None, ge=1990, le=2100)
    price: int | None = Field(default=None, gt=0)
    fuel_type: str | None = Field(default=None, min_length=3, max_length=20)
    transmission: str | None = Field(default=None, min_length=3, max_length=20)
    kilometers: int | None = Field(default=None, ge=0)
    owner_count: int | None = Field(default=None, ge=1, le=10)
    color: str | None = Field(default=None, min_length=3, max_length=30)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=1000)
    image_path: str | None = None
    is_available: bool | None = None

class CarResponse(CarBase):
    id: int
    user_id: int
    image_path: str
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CarListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    cars: list[CarResponse]