from pydantic import BaseModel, Field
from typing import Optional, List

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Code snippet to analyze", min_length=1)
    language: str = Field(..., description="Programming language", examples=["python", "javascript", "java"])
    context: Optional[str] = Field(None, description="Additional context about the code")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "code": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr",
                "language": "python",
                "context": "Sorting algorithm implementation"
            }]
        }
    }

class CodeAnalysisResponse(BaseModel):
    analysis: str = Field(..., description="Detailed code analysis and explanation")
    complexity: Optional[str] = Field(None, description="Time/space complexity analysis")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    patterns_detected: List[str] = Field(default_factory=list, description="Design patterns identified")
    
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
