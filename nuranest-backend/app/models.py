from pydantic import BaseModel, Field
from typing import Optional,List
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
    symptom_combinations: list = Field(None, description="List of matched symptom combinations, if any")
    timeline_conditions: list = Field(None, description="List of matched conditions based on symptom timeline rules, if any")
    combination_inferences: list = Field(None, description="List of inferred symptom combinations from user input")
    classifications: list = Field(None, description="List of classified symptoms from the question")
    timeline_results: list = Field(None, description="List of conditions matched by week in the pregnancy timeline")
    combination_results: list = Field(None, description="List of inferred symptom combinations based on user input")
    sources: Optional[list] = Field(None, description="List of sources used to generate the answer")
    confidence_score: Optional[float] = Field(None, description="Confidence score of the answer")
    processing_time: float = Field(..., description="Time taken to process the question in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the response")
    # sources: Optional[List[str]] = Field(None, description="List of sources used for the answer")
    markdown_summary: Optional[str] = Field(None, description="Markdown formatted triage table with visual risk levels")
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "💡 During pregnancy, you should avoid raw fish, unpasteurized dairy products, high-mercury fish, raw eggs, and undercooked meat. 📋 Key recommendations: • Avoid raw or undercooked seafood • Stay away from unpasteurized dairy • Limit high-mercury fish consumption • Cook eggs thoroughly ⚠️ **Medical Disclaimer:** This information is for educational purposes only. Always consult with your healthcare provider for personalized medical advice.",
                "symptom_combinations": [
                    {   
                        "condition": "Preeclampsia",
                        "risk": "High",
                        "action": "Seek immediate medical attention",
                        "matched_symptoms": ["headache", "swelling"]
                    },
                ],
                "timeline_conditions": [
                    {
                        "symptom": "nausea",
                        "condition": "Normal pregnancy symptom",
                        "risk": "Low",
                        "action": "Monitor symptoms",
                        "week": 6
                    }
                ],
                "combination_inferences": [
                    {
                        "condition": "Normal 1st trimester symptoms",
                        "risk": "Low",
                        "action": "Self-monitor, routine prenatal follow-up",
                        "matched_symptoms": ["mild nausea", "fatigue", "breast tenderness"]
                    }
                ],
                "classifications": [
                    {
                        "matched_phrase": "mild nausea",
                        "condition": "Normal 1st trimester symptom",
                        "risk": "Low",
                        "action": "Self-monitor, routine prenatal follow-up"
                    }
                ],
                "timeline_results": [
                    {
                        "symptom": "mild nausea",
                        "condition": "Normal 1st trimester symptom",
                        "risk": "Low",
                        "action": "Self-monitor, routine prenatal follow-up",
                        "week": 6
                    }
                ],
                "combination_results": [
                    {
                        "matched_symptoms": ["mild nausea", "fatigue", "breast tenderness"],
                        "condition": "Normal 1st trimester symptoms",
                        "risk": "Low",
                        "action": "Self-monitor, routine prenatal follow-up"
                    }
                ],
                "sources": ["https://www.acog.org/womens-health/faqs/nutrition-during-pregnancy"],
                "confidence_score": 0.92,
                "processing_time": 1.5,
                "timestamp": "2024-01-15T10:30:00Z",
                "sources": [
                    "WHO Guidelines for Pregnancy Care",
                    "American College of Obstetricians and Gynecologists",
                    "Mayo Clinic Pregnancy Information"
                ],
                "markdown_summary": "### Triage Summary\n\n| Condition | Risk Level | Action | Symptoms |\n|-----------|------------|--------|----------|\n| Preeclampsia | 🟥 High | Seek immediate medical attention | headache, swelling |\n| Normal pregnancy symptom | 🟢 Low | Monitor symptoms | nausea |\n| Normal 1st trimester symptoms | 🟢 Low | Self-monitor, routine prenatal follow-up | mild nausea, fatigue, breast tenderness |\n"
            }
        } 