from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class DisplayInfo(BaseModel):
    rating: float = Field(ge=0.0, le=5.0)
    sales_count: int = Field(ge=0)
    discount_percentage: float = Field(ge=0.0, le=100.0)


# Request Models
class ProductCreateRequest(BaseModel):
    name: str
    description: str
    category: str
    image_url: Optional[str] = None
    price: float = Field(gt=0)
    stock_available: int = Field(ge=0)
    stock_unit: str
    stock_warning_threshold: int = Field(ge=0)
    status: str = "active"


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_available: Optional[int] = Field(None, ge=0)
    stock_unit: Optional[str] = None
    stock_warning_threshold: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None


# Response Models
class ProductResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    category: str
    image_url: Optional[str] = None
    price: float
    stock_available: int
    stock_unit: str
    stock_warning_threshold: int
    display_info: DisplayInfo
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int
