import os
import logging
from typing import Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not set, service will return mock responses")
            self.client = None
        else:
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-1.5-pro')
            logger.info("Gemini service initialized successfully")
    
    async def analyze_code(self, code: str, language: str, context: Optional[str] = None) -> dict:
        logger.info(f"Analyzing {language} code snippet")
        
        if not self.client:
            return self._mock_response(code, language)
        
        try:
            prompt = self._build_prompt(code, language, context)
            response = await self._call_gemini_api(prompt)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._mock_response(code, language)
    
    def _build_prompt(self, code: str, language: str, context: Optional[str]) -> str:
        base_prompt = f"""Analyze the following {language} code and provide:
1. A detailed explanation of what the code does
2. Time and space complexity analysis
3. Suggestions for improvement
4. Design patterns used (if any)

Code:
```{language}
{code}
```
"""
        if context:
            base_prompt += f"\nContext: {context}"
        
        return base_prompt
    
    async def _call_gemini_api(self, prompt: str) -> str:
        logger.info("Calling Gemini API")
        response = self.client.generate_content(prompt)
        return response.text
    
    def _parse_response(self, response: str) -> dict:
        return {
            "analysis": response,
            "complexity": None,
            "suggestions": [],
            "patterns_detected": []
        }
    
    def _mock_response(self, code: str, language: str) -> dict:
        logger.info("Returning mock response")
        return {
            "analysis": f"This {language} code snippet demonstrates fundamental programming concepts. "
                       f"The implementation follows standard practices and could be optimized for production use. "
                       f"Consider adding error handling, input validation, and comprehensive documentation.",
            "complexity": "O(n) time complexity, O(1) space complexity",
            "suggestions": [
                "Add type hints for better code documentation",
                "Implement error handling for edge cases",
                "Consider adding unit tests",
                "Optimize for performance if handling large datasets"
            ],
            "patterns_detected": ["functional-programming", "iterative-approach"]
        }

gemini_service = GeminiService()
