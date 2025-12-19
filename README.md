# Sharing Session Knowledge API

REST API yang dibangun menggunakan FastAPI, MongoDB, dan JWT Authentication dengan struktur proyek yang modular.


## 📋 Fitur

- ✅ **Authentication & Authorization**: JWT-based authentication dengan Bearer Token
- ✅ **User Management**: CRUD lengkap untuk pengelolaan user
- ✅ **Product Management**: CRUD lengkap untuk pengelolaan produk dengan auto-generated display_info
- ✅ **File Upload**: Upload gambar untuk profile user dan produk
- ✅ **API Documentation**: Swagger UI otomatis tersedia di `/docs`
- ✅ **Database**: MongoDB dengan driver async (Motor)
- ✅ **Password Security**: Password di-hash menggunakan bcrypt

## 🛠️ Teknologi yang Digunakan

- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn
- **Database**: MongoDB (Motor untuk async operations)
- **Authentication**: JWT dengan python-jose
- **Password Hashing**: passlib[bcrypt]
- **Validation**: Pydantic
- **Environment**: python-dotenv

## 🎥 Screen Recording Demo

Demo penggunakan API via Swagger:

👉 **[Akses Screen Recording](https://drive.google.com/drive/folders/1J3529zVh32QId37WfQXnk4cVmsxOwRdX?usp=drive_link)**

Video ini menunjukkan:
- ✅ Penggunaan Swagger UI untuk testing
- ✅ Cara login dan menggunakan JWT
- ✅ Operasi CRUD untuk users & products
- ✅ Upload dan akses gambar users & products
- ✅ Testing endpoint yang ada

## 📁 Struktur Proyek

```
service/
├── app/
│   ├── api/              # API routes
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py      # User endpoints
│   │   ├── products.py   # Product endpoints
│   │   └── dependencies.py  # Dependency injection (JWT)
│   ├── core/             # Core configurations
│   │   ├── config.py     # Settings & environment variables
│   │   └── security.py   # JWT & password utilities
│   ├── db/               # Database connection
│   │   └── connection.py # MongoDB connection
│   ├── models/           # Pydantic models (schemas)
│   │   ├── user.py       # User schemas (Request/Response)
│   │   └── product.py    # Product schemas (Request/Response)
│   ├── services/         # Business logic
│   │   ├── user_service.py
│   │   └── product_service.py
│   └── utils/            # Utilities
│       ├── file_upload.py
│       └── helpers.py
├── main.py               # Entry point aplikasi
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (buat file ini)
└── README.md
```

## 🚀 Cara Memulai Proyek

### Prasyarat

Pastikan Anda sudah menginstall:
- Python 3.8 atau lebih tinggi
- MongoDB (local atau remote)
- pip (Python package manager)

### Langkah 1: Clone Repository

```bash
git clone <repository-url>
cd service
```

### Langkah 2: Buat Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Langkah 4: Setup Environment Variables

Buat file `.env` di root directory dengan konten berikut:

```env
MONGODB_URL=mongodb://localhost:27017/fullstack_sharing_knowledge
JWT_SECRET_KEY=your-secret-key-here-minimal-32-characters-long-for-security
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Penjelasan:**
- `MONGODB_URL`: URL koneksi MongoDB (default: `mongodb://localhost:27017/fullstack_sharing_knowledge`)
- `JWT_SECRET_KEY`: Secret key untuk signing JWT token (gunakan string acak yang panjang, minimal 32 karakter)
- `JWT_ALGORITHM`: Algoritma untuk JWT (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Durasi token berlaku dalam menit (default: 30)

**⚠️ Penting**: Jangan commit file `.env` ke repository! File ini sudah ada di `.gitignore`.

### Langkah 5: Pastikan MongoDB Berjalan

**Jika menggunakan MongoDB lokal:**
```bash
# Windows
mongod

# Linux/Mac
sudo systemctl start mongod
# atau
mongod
```

**Atau gunakan MongoDB Atlas (cloud):**
- Daftar di [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Dapatkan connection string
- Gunakan connection string sebagai `MONGODB_URL` di `.env`

### Langkah 6: Jalankan Server

**Cara 1: Menggunakan uvicorn langsung**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Cara 2: Menggunakan Python**
```bash
python main.py
```

**Cara 3: Menggunakan uvicorn dengan reload (development)**
```bash
uvicorn main:app --reload
```

Server akan berjalan di: `http://localhost:8000`

## 📚 API Documentation

Setelah server berjalan, Anda dapat mengakses:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Endpoint API

### Authentication

- `POST /api/v1/auth/login` - Login dan mendapatkan JWT token

### Users (Memerlukan JWT Token)

- `GET /api/v1/users` - Mendapatkan semua users (dengan pagination)
- `GET /api/v1/users/{user_id}` - Mendapatkan user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Hapus user

### Products (Memerlukan JWT Token)

- `GET /api/v1/products` - Mendapatkan semua products (dengan pagination)
- `GET /api/v1/products/{product_id}` - Mendapatkan product by ID
- `POST /api/v1/products` - Membuat product baru (display_info auto-generated)
- `PUT /api/v1/products/{product_id}` - Update product (display_info auto-regenerated)
- `DELETE /api/v1/products/{product_id}` - Hapus product

## 🔑 Cara Menggunakan API

### 1. Login

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "name": "John Doe",
    "email": "user@example.com",
    ...
  }
}
```

### 2. Menggunakan Token

Untuk semua endpoint yang memerlukan authentication, tambahkan header:

```
Authorization: Bearer <your-access-token>
```

Contoh dengan curl:
```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/v1/users
```

## 📝 Catatan Penting

### Display Info (Products)

Field `display_info` pada Product akan **otomatis di-generate** oleh sistem saat:
- **POST** `/api/v1/products` - Membuat product baru
- **PUT** `/api/v1/products/{product_id}` - Update product

Nilai yang di-generate:
- `rating`: 4.7 - 5.0 (random)
- `sales_count`: 50 - 150 (random)
- `discount_percentage`: 0 - 30 (random)

**User tidak bisa mengirim nilai `display_info` melalui payload**. Sistem akan selalu meng-overwrite nilai ini.

### File Upload

Gambar yang di-upload akan disimpan di folder `uploads/` dengan struktur:
- User profile images: `uploads/users/`
- Product images: `uploads/products/`

Pastikan folder `uploads/` sudah ada atau sistem akan membuatnya secara otomatis.

## 🐛 Troubleshooting

### Error: MongoDB connection failed
- Pastikan MongoDB sudah berjalan
- Periksa `MONGODB_URL` di file `.env`
- Pastikan format URL benar: `mongodb://localhost:27017/database_name`

### Error: JWT_SECRET_KEY not found
- Pastikan file `.env` sudah dibuat
- Pastikan `JWT_SECRET_KEY` sudah diisi dengan nilai minimal 32 karakter

### Error: Module not found
- Pastikan virtual environment sudah diaktifkan
- Install ulang dependencies: `pip install -r requirements.txt`

### Port 8000 sudah digunakan
- Ganti port di command: `uvicorn main:app --reload --port 8001`
- Atau ubah port di `main.py`

## 📦 Development

### Menjalankan di Development Mode

```bash
uvicorn main:app --reload
```

Flag `--reload` akan otomatis restart server saat ada perubahan kode.

### Production Deployment

Untuk production, disarankan untuk:
1. Set `JWT_SECRET_KEY` dengan nilai yang kuat dan random
2. Gunakan environment variables dari hosting provider
3. Konfigurasi CORS dengan domain spesifik
4. Gunakan reverse proxy (nginx) dengan HTTPS
5. Set up proper logging dan monitoring


## 👥 Kontributor

Nada Yumna

---

**Happy Coding! 🚀**
