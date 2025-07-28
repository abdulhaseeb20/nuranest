import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import api_router
from app.services import pregnancy_service

# Hugging Face Spaces configuration
import os
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("PORT", "7860")

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting Nuranest Pregnancy AI API...")
    logger.info(f"📡 Server will be available at: http://{settings.host}:{settings.port}")
    logger.info(f"📚 API Documentation: http://{settings.host}:{settings.port}/docs")
    
    # Initialize the AI service
    logger.info("🔧 Initializing AI service...")
    try:
        success = await pregnancy_service.initialize()
        if success:
            logger.info("✅ AI service initialized successfully")
        else:
            logger.warning("⚠️ AI service initialization failed - will need manual initialization")
    except Exception as e:
        logger.error(f"❌ AI service initialization error: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Nuranest Pregnancy AI API...")

# Create FastAPI app
app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": exc.errors(),
            "status_code": 422,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"General Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "status_code": 500,
            "timestamp": time.time()
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Nuranest Pregnancy AI API",
        "version": settings.version,
        "description": settings.description,
        "documentation": "/docs",
        "status": "running"
    }

# Include API routes
app.include_router(api_router) 