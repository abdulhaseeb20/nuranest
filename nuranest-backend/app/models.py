from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    """Request model for asking pregnancy health questions"""
    question: str = Field(..., description="The pregnancy health question to ask", min_length=1, max_length=1000)
    
    class Config:
        schema_extra = {
            "example": {
                "question": "What foods should I avoid during pregnancy?"
            }
        }

class QuestionResponse(BaseModel):
    """Response model for pregnancy health questions"""
    answer: str = Field(..., description="AI-generated answer to the question")
    confidence_score: Optional[float] = Field(None, description="Confidence score of the answer")
    processing_time: float = Field(..., description="Time taken to process the question in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the response")
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "💡 During pregnancy, you should avoid raw fish, unpasteurized dairy products, high-mercury fish, raw eggs, and undercooked meat. 📋 Key recommendations: • Avoid raw or undercooked seafood • Stay away from unpasteurized dairy • Limit high-mercury fish consumption • Cook eggs thoroughly ⚠️ **Medical Disclaimer:** This information is for educational purposes only. Always consult with your healthcare provider for personalized medical advice.",
                "confidence_score": 0.92,
                "processing_time": 1.5,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        } 