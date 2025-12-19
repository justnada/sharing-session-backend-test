from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, File
from typing import Optional, Union
from app.models.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
    ProductListResponse
)
from app.api.dependencies import get_current_user
from app.services.product_service import (
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product
)
from app.utils.file_upload import save_uploaded_file
import json
from pydantic import ValidationError
from app.utils.form_data import as_form_product_create, as_form_product_update

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user)
):
    """Mengambil semua products (dengan pagination)"""
    products, total = await get_all_products(skip=skip, limit=limit)
    return ProductListResponse(products=products, total=total)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mengambil product berdasarkan ID"""
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product_route(
    file: UploadFile = File(None),
    product_data: ProductCreateRequest = Depends(as_form_product_create), 
    current_user: dict = Depends(get_current_user)  
):
    if file:
        file_url = await save_uploaded_file(file, "products")
        product_data.image_url = file_url

    product = await create_product(product_data)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_route(
    product_id: str,
    file: UploadFile = File(None), 
    product_data: ProductUpdateRequest = Depends(as_form_product_update),
    current_user: dict = Depends(get_current_user)
):
    """Update product"""
    
    if file and file.filename:
        file_url = await save_uploaded_file(file, "products")
        product_data.image_url = file_url

    updated_product = await update_product(product_id, product_data)
    
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    return updated_product


@router.delete("/{product_id}")
async def delete_product_route(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Hapus product"""
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return {"message": "Product deleted successfully"}
