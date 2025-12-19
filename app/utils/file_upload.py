import os
import aiofiles
from fastapi import UploadFile, HTTPException, status
from datetime import datetime
import uuid


UPLOAD_DIR = "uploads"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


async def save_uploaded_file(file: UploadFile, subfolder: str = "") -> str:
    """
    Save uploaded file dan return URL relative path
    subfolder: 'users' atau 'products'
    """
    # Validasi extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension not allowed. Allowed: {ALLOWED_IMAGE_EXTENSIONS}"
        )
    
    # Buat folder jika belum ada
    upload_path = os.path.join(UPLOAD_DIR, subfolder) if subfolder else UPLOAD_DIR
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{timestamp}_{unique_id}{file_ext}"
    file_path = os.path.join(upload_path, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Return relative URL path
    return f"{upload_path}/{filename}"
