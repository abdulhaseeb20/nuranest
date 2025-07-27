from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import logging

from .models import (
    QuestionRequest, 
    QuestionResponse
)
from .services import pregnancy_service
from .config import settings

logger = logging.getLogger(__name__)

# Create routers
api_router = APIRouter(prefix=settings.api_prefix)
ai_router = APIRouter(prefix="/ai", tags=["AI"])

# AI endpoints
@ai_router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a pregnancy health question"""
    try:
        if not pregnancy_service.is_initialized:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service not initialized. Please initialize the service first."
            )
        
        response = await pregnancy_service.ask_question(
            question=request.question
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process question: {str(e)}"
        )

# Include AI router in the main API router
api_router.include_router(ai_router) 