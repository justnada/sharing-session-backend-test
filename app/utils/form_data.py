from fastapi import Form
from typing import Optional
from app.models.product import ProductCreateRequest, ProductUpdateRequest
from app.models.user import UserCreateRequest, UserUpdateRequest


def as_form_user_create(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    status: str = Form("active")
) -> UserCreateRequest:
    return UserCreateRequest(
        name=name,
        email=email,
        phone=phone,
        password=password,
        status=status
    )


def as_form_user_update(
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    status: Optional[str] = Form(None)
) -> UserUpdateRequest:
    return UserUpdateRequest (
        name=name,
        email=email,
        phone=phone,
        status=status
    )

def as_form_product_create(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    price: float = Form(..., gt=0),
    stock_available: int = Form(..., ge=0),
    stock_unit: str = Form(...),
    stock_warning_threshold: int = Form(..., ge=0),
    status: str = Form("active")
) -> ProductCreateRequest:
    return ProductCreateRequest(
        name=name,
        description=description,
        category=category,
        price=price,
        stock_available=stock_available,
        stock_unit=stock_unit,
        stock_warning_threshold=stock_warning_threshold,
        status=status
    )


def as_form_product_update(
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    price: Optional[str] = Form(None), 
    stock_available: Optional[str] = Form(None),
    stock_unit: Optional[str] = Form(None),
    stock_warning_threshold: Optional[str] = Form(None),
    status: Optional[str] = Form(None)
) -> ProductUpdateRequest:
    def clean(val):
        if val == "" or val is None:
            return None
        return val

    return ProductUpdateRequest(
        name=clean(name),
        description=clean(description),
        category=clean(category),
        price=float(price) if clean(price) else None,
        stock_available=int(stock_available) if clean(stock_available) else None,
        stock_unit=clean(stock_unit),
        stock_warning_threshold=int(stock_warning_threshold) if clean(stock_warning_threshold) else None,
        status=clean(status)
    )