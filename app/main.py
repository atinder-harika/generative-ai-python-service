from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analysis
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Generative AI Code Analysis Service",
    description="AI-powered code documentation and analysis using Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "generative-ai-service"}

@app.get("/")
async def root():
    return {
        "message": "Generative AI Code Analysis Service",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
