from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, File
from typing import Optional
from app.models.user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UserListResponse
)
from app.api.dependencies import get_current_user
from app.services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from app.utils.file_upload import save_uploaded_file
from app.utils.form_data import as_form_user_create, as_form_user_update

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(
    file: UploadFile = File(None),
    user_data: UserCreateRequest = Depends(as_form_user_create)
):
    """Membuat user baru"""
    
    if file:
        file_url = await save_uploaded_file(file, "users")
        user_data.profile_img = file_url
    
    user = await create_user(user_data)
    return user

@router.get("", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user)
):
    """Mengambil semua users (dengan pagination)"""
    users, total = await get_all_users(skip=skip, limit=limit)
    return UserListResponse(users=users, total=total)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mengambil user berdasarkan ID"""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user



@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(
    user_id: str,
    file: UploadFile = File(None),
    user_data: UserUpdateRequest = Depends(as_form_user_update),
    current_user: dict = Depends(get_current_user)
):
    """Update user"""
    
    if file:
        file_url = await save_uploaded_file(file, "users")
        user_data.profile_img = file_url

    updated_user = await update_user(user_id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}")
async def delete_user_route(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Hapus user"""
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
