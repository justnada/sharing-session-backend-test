from typing import Optional
import os
from pathlib import Path
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException, status
from app.db.connection import get_database
from app.core.security import get_password_hash, verify_password
from app.models.user import UserCreateRequest, UserUpdateRequest, UserResponse


async def create_user(user_data: UserCreateRequest) -> UserResponse:
    """Membuat user baru dengan validasi email unique"""
    db = get_database()
    users_collection = db.users
    
    # Check if email already exists
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Buat document user
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "phone": user_data.phone,
        "password": hashed_password,
        "profile_img": user_data.profile_img,
        "status": user_data.status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    # Hapus password dari response
    user_doc.pop("password")
    return UserResponse(**user_doc)


async def get_user_by_email(email: str) -> Optional[dict]:
    """Mengambil user berdasarkan email"""
    db = get_database()
    users_collection = db.users
    user = await users_collection.find_one({"email": email})
    return user


async def get_user_by_id(user_id: str) -> Optional[UserResponse]:
    """Mengambil user berdasarkan ID"""
    db = get_database()
    users_collection = db.users
    
    if not ObjectId.is_valid(user_id):
        return None
    
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    
    # Hapus password dari response
    user.pop("password", None)
    return UserResponse(**user)


async def get_all_users(skip: int = 0, limit: int = 100) -> tuple[list[UserResponse], int]:
    """Mengambil semua users dengan pagination"""
    db = get_database()
    users_collection = db.users
    
    # Hitung total
    total = await users_collection.count_documents({})
    
    # Ambil users
    cursor = users_collection.find({}).skip(skip).limit(limit)
    users = []
    
    async for user in cursor:
        user.pop("password", None)  # Hapus password
        users.append(UserResponse(**user))
    
    return users, total


async def update_user(user_id: str, user_data: UserUpdateRequest) -> Optional[UserResponse]:
    """Update user dengan pembersihan foto profil lama"""
    db = get_database()
    users_collection = db.users
    
    if not ObjectId.is_valid(user_id):
        return None
    
    old_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not old_user:
        return None
    
    update_data = {k: v for k, v in user_data.model_dump(exclude_unset=True).items() if v is not None}
    
    # Clean image
    if "profile_img" in update_data and update_data["profile_img"]:
        old_profile_path = old_user.get("profile_img")
        
        if old_profile_path and old_profile_path != update_data["profile_img"]:
            file_to_delete = Path(old_profile_path)
            
            try:
                if file_to_delete.exists() and file_to_delete.is_file():
                    os.remove(file_to_delete)
                    print(f"DEBUG: Foto profil lama berhasil dihapus: {file_to_delete}")
            except Exception as e:
                print(f"WARNING: Gagal menghapus file fisik foto profil: {e}")

    if not update_data:
        return None
    
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        return None
    
    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if updated_user:
        updated_user.pop("password", None)
        return UserResponse(**updated_user)
        
    return None


async def delete_user(user_id: str) -> bool:
    """Hapus user"""
    db = get_database()
    users_collection = db.users
    
    if not ObjectId.is_valid(user_id):
        return False
    
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0


async def verify_user_credentials(email: str, password: str) -> Optional[dict]:
    """Verifikasi credentials user"""
    user = await get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user["password"]):
        return None

    # Limit status user
    if user.get("status") == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive. Please contact administrator."
        )
    
    # Hapus password sebelum return
    user.pop("password")
    return user
