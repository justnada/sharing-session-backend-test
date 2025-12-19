from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId
from pathlib import Path
import os
from app.db.connection import get_database
from app.models.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from app.utils.helpers import generate_display_info


async def create_product(product_data: ProductCreateRequest) -> ProductResponse:
    """Membuat product baru dengan display_info auto-generated"""
    db = get_database()
    products_collection = db.products
    
    # Generate display_info otomatis
    display_info = generate_display_info()
    
    # Buat document product
    product_doc = {
        "name": product_data.name,
        "description": product_data.description,
        "category": product_data.category,
        "image_url": product_data.image_url,
        "price": product_data.price,
        "stock_available": product_data.stock_available,
        "stock_unit": product_data.stock_unit,
        "stock_warning_threshold": product_data.stock_warning_threshold,
        "display_info": display_info,
        "status": product_data.status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await products_collection.insert_one(product_doc)
    product_doc["_id"] = result.inserted_id
    
    return ProductResponse(**product_doc)


async def get_product_by_id(product_id: str) -> Optional[ProductResponse]:
    """Mengambil product berdasarkan ID"""
    db = get_database()
    products_collection = db.products
    
    if not ObjectId.is_valid(product_id):
        return None
    
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return None
    
    return ProductResponse(**product)


async def get_all_products(skip: int = 0, limit: int = 100) -> tuple[list[ProductResponse], int]:
    """Mengambil semua products dengan pagination"""
    db = get_database()
    products_collection = db.products
    
    # Hitung total
    total = await products_collection.count_documents({})
    
    # Ambil products
    cursor = products_collection.find({}).skip(skip).limit(limit)
    products = []
    
    async for product in cursor:
        products.append(ProductResponse(**product))
    
    return products, total


# async def update_product(product_id: str, product_data: ProductUpdateRequest) -> Optional[ProductResponse]:
#     """Update product dengan display_info auto-regenerated"""
#     db = get_database()
#     products_collection = db.products
    
#     if not ObjectId.is_valid(product_id):
#         return None
    
#     # Build update dict (hanya field yang ada)
#     update_data = {k: v for k, v in product_data.model_dump(exclude_unset=True).items() if v is not None}
    
#     if not update_data:
#         return None
    
#     # Generate display_info baru otomatis untuk PUT
#     display_info = generate_display_info()
#     update_data["display_info"] = display_info
#     update_data["updated_at"] = datetime.utcnow()
    
#     result = await products_collection.update_one(
#         {"_id": ObjectId(product_id)},
#         {"$set": update_data}
#     )
    
#     if result.matched_count == 0:
#         return None
    
#     # Ambil product yang sudah diupdate
#     updated_product = await products_collection.find_one({"_id": ObjectId(product_id)})
#     return ProductResponse(**updated_product)

async def update_product(product_id: str, product_data: ProductUpdateRequest) -> Optional[dict]:
    """Update product dengan auto-cleanup gambar lama dan regenerasi display_info"""
    db = get_database()
    products_collection = db.products
    
    if not ObjectId.is_valid(product_id):
        return None
    
    # Ambil data produk lama untuk mendapatkan path gambar lama
    old_product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not old_product:
        return None

    # Ambil data yang dikirim oleh user (mengabaikan field yang tidak dikirim)
    update_data = product_data.model_dump(exclude_unset=True)
    
    # Pembersihan Gambar Lama
    if "image_url" in update_data and update_data["image_url"]:
        old_image_path = old_product.get("image_url")
        
        # Cek jika sebelumnya memang sudah ada gambar (bukan None/kosong)
        if old_image_path:
            file_to_delete = Path(old_image_path)
            
            try:
                if file_to_delete.exists() and file_to_delete.is_file():
                    os.remove(file_to_delete)
                    print(f"DEBUG: File lama berhasil dihapus: {file_to_delete}")
            except Exception as e:
                print(f"WARNING: Gagal menghapus file fisik: {e}")

   
    if not update_data and not "image_url" in update_data:
        return old_product
    
    # Tambahkan metadata otomatis (regenerate display_info)
    update_data["display_info"] = generate_display_info()
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    
    updated_doc = await products_collection.find_one({"_id": ObjectId(product_id)})
    return updated_doc
    

async def delete_product(product_id: str) -> bool:
    """Hapus product"""
    db = get_database()
    products_collection = db.products
    
    if not ObjectId.is_valid(product_id):
        return False
    
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0
