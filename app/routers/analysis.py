from fastapi import APIRouter, HTTPException
from app.models.schemas import CodeAnalysisRequest, CodeAnalysisResponse, ErrorResponse
from app.services.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/analyze",
    response_model=CodeAnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze code snippet",
    description="Submit code for AI-powered analysis and documentation generation"
)
async def analyze_code(request: CodeAnalysisRequest):
    try:
        logger.info(f"Received analysis request for {request.language} code")
        
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        result = await gemini_service.analyze_code(
            code=request.code,
            language=request.language,
            context=request.context
        )
        
        return CodeAnalysisResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
