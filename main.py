from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.connection import connect_to_mongo, close_mongo_connection
from app.api import auth, users, products
import os
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events untuk startup dan shutdown"""
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()


# Inisialisasi FastAPI app
app = FastAPI(
    title="Fullstack Sharing Knowledge API",
    description="REST API dengan FastAPI, MongoDB, dan JWT Authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mounting static files
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Fullstack Sharing Knowledge API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2500, reload=True)
