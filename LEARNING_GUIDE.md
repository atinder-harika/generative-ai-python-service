# Learning Guide: FastAPI & Generative AI Integration

Comprehensive learning path for building production-ready FastAPI services integrated with AI APIs.

---

## Table of Contents

1. [FastAPI Fundamentals](#fastapi-fundamentals)
2. [Async Python Programming](#async-python-programming)
3. [Pydantic & Data Validation](#pydantic--data-validation)
4. [Gemini AI API Integration](#gemini-ai-api-integration)
5. [Testing Async Applications](#testing-async-applications)
6. [Deployment Strategies](#deployment-strategies)
7. [Future Enhancements](#future-enhancements)

---

## FastAPI Fundamentals

### Core Concepts

**Why FastAPI?**
- Automatic API documentation (Swagger UI, ReDoc)
- Built-in data validation via Pydantic
- Async/await support for high concurrency
- Type hints for better IDE support
- High performance (comparable to Node.js, Go)

**Basic Application Structure:**
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run with: uvicorn main:app --reload
```

### Path Operations & Request Handling

**GET Request:**
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**POST Request with Request Body:**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Dependency Injection

```python
async def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def read_users(db: Database = Depends(get_db)):
    return db.get_all_users()
```

### Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return items[item_id]
```

**Learning Exercise:**
- Create a simple CRUD API with in-memory storage
- Add query parameters for filtering
- Implement proper error responses
- Test with Swagger UI at `/docs`

---

## Async Python Programming

### Understanding Async/Await

**Synchronous vs Asynchronous:**
```python
# Synchronous (blocks execution)
def fetch_data():
    response = requests.get("https://api.example.com/data")
    return response.json()

# Asynchronous (non-blocking)
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### Event Loop & Concurrency

```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1 done"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 done"

# Run tasks concurrently
async def main():
    results = await asyncio.gather(task1(), task2())
    print(results)

# Output: ['Task 1 done', 'Task 2 done'] after 2 seconds (not 3)
```

### When to Use Async

**Use Async For:**
- I/O-bound operations (API calls, database queries, file I/O)
- High concurrency requirements
- Real-time applications

**Don't Use Async For:**
- CPU-bound operations (heavy computations)
- Simple scripts with sequential logic
- When synchronous code is clearer

**Learning Exercise:**
- Convert synchronous API calls to async
- Measure performance difference with concurrent requests
- Practice error handling in async functions

---

## Pydantic & Data Validation

### Model Definition

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    age: Optional[int] = Field(None, ge=0, le=150)
    tags: List[str] = []
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "age": 30,
                "tags": ["developer", "python"]
            }]
        }
    }
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class UserWithAddress(BaseModel):
    name: str
    address: Address

# Usage
user = UserWithAddress(
    name="John",
    address={"street": "123 Main St", "city": "NYC", "country": "USA"}
)
```

### Response Models

```python
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # password excluded from response

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # password hashing logic here
    return UserResponse(id=1, username=user.username, email=user.email)
```

**Learning Exercise:**
- Create complex nested models
- Add custom validators
- Use Field() for constraints
- Test validation errors in Swagger UI

---

## Gemini AI API Integration

### Setting Up Gemini

**Installation:**
```bash
pip install google-generativeai
```

**Basic Configuration:**
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')
```

### Generating Content

**Simple Generation:**
```python
response = model.generate_content("Explain quantum computing")
print(response.text)
```

**Streaming Response:**
```python
response = model.generate_content("Write a story", stream=True)
for chunk in response:
    print(chunk.text, end='')
```

### Advanced Prompting

**System Instructions:**
```python
model = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction="You are a Python expert. Answer concisely."
)
```

**Structured Prompts:**
```python
prompt = """Analyze this code:
```python
{code}
```

Provide:
1. Functionality explanation
2. Time complexity
3. Improvement suggestions
"""
response = model.generate_content(prompt.format(code=user_code))
```

### Error Handling & Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_gemini_with_retry(prompt: str):
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise
```

**Learning Exercise:**
- Get Gemini API key from Google AI Studio
- Experiment with different prompts
- Implement streaming responses
- Add rate limiting and retry logic
- Compare response quality with different models

---

## Testing Async Applications

### Test Client Setup

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
```

### Testing Async Endpoints

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/analyze", json={"code": "test"})
    assert response.status_code == 200
```

### Mocking External APIs

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_gemini_service():
    with patch('app.services.gemini_service.genai') as mock_genai:
        mock_response = AsyncMock()
        mock_response.text = "Mocked analysis"
        mock_genai.GenerativeModel.return_value.generate_content_async.return_value = mock_response
        
        result = await gemini_service.analyze_code("test code", "python")
        assert "analysis" in result
```

### Coverage & Reports

```bash
# Run with coverage
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html
```

**Learning Exercise:**
- Write tests for all endpoints
- Mock Gemini API responses
- Achieve 80%+ code coverage
- Test error scenarios

---

## Deployment Strategies

### Docker Deployment

**Multi-stage Build:**
```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ ./app/
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Cloud Deployment Options

**1. AWS Lambda + API Gateway:**
- Use Mangum for ASGI to Lambda adapter
- Configure API Gateway for HTTP endpoints
- Set environment variables in Lambda console

**2. Google Cloud Run:**
- Fully managed container platform
- Auto-scaling based on traffic
- Pay per request pricing

**3. Railway / Render:**
- Simple git push deployment
- Automatic HTTPS
- Environment variable management

**Learning Exercise:**
- Deploy to Railway or Render
- Set up environment variables
- Configure custom domain
- Monitor logs and metrics

---

## Future Enhancements

### 1. Streaming Responses
```python
from fastapi.responses import StreamingResponse

@app.post("/analyze/stream")
async def analyze_stream(request: CodeAnalysisRequest):
    async def generate():
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            yield f"data: {chunk.text}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 2. Caching Layer
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_analysis(code_hash: str):
    # Redis or in-memory cache
    pass
```

### 3. Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze_code(request: Request, data: CodeAnalysisRequest):
    pass
```

### 4. Database Integration
- Store analysis history
- User authentication
- Usage analytics

### 5. WebSocket Support
- Real-time code analysis
- Collaborative features

### 6. Multiple AI Providers
- Fallback to OpenAI if Gemini fails
- Model comparison
- Cost optimization

---

## Resources

**Official Documentation:**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/latest/)
- [Google AI Studio](https://makersuite.google.com/)

**Books & Tutorials:**
- "Python Concurrency with asyncio" by Matthew Fowler
- FastAPI course on Test-Driven.io
- Real Python FastAPI tutorials

**Tools:**
- Postman for API testing
- httpie for CLI testing
- Swagger Editor for API design

---

## Progress Checklist

- [ ] Build basic FastAPI application
- [ ] Add Pydantic models with validation
- [ ] Implement async database queries
- [ ] Integrate Gemini AI API
- [ ] Write unit and integration tests
- [ ] Set up CI/CD pipeline
- [ ] Deploy to cloud platform
- [ ] Add caching layer
- [ ] Implement rate limiting
- [ ] Monitor production metrics
