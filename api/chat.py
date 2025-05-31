import os
import json
import logging
import asyncio
import traceback
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

import aiohttp
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

# Configure logging for Vercel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
try:
    logger.info("Loading environment variables from .env file...")
    load_dotenv()
    logger.info("Environment variables loaded")
except Exception as e:
    logger.error(f"Error loading environment variables: {str(e)}")
    logger.error(traceback.format_exc())

# Environment variables with defaults
try:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not found in environment variables")
    else:
        logger.info(f"OPENROUTER_API_KEY found: {OPENROUTER_API_KEY[:8]}...")

    MODEL = os.getenv("MODEL", "deepseek/deepseek-chat")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

    logger.info(f"Configuration: MODEL={MODEL}, MAX_TOKENS={MAX_TOKENS}, TEMPERATURE={TEMPERATURE}")
    logger.info(f"API Key configured: {bool(OPENROUTER_API_KEY)}")
except Exception as e:
    logger.error(f"Error configuring environment variables: {str(e)}")
    logger.error(traceback.format_exc())

app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Serve static files from public directory
try:
    app.mount("/public", StaticFiles(directory="public", html=True), name="public")
except Exception as e:
    logger.error(f"Error mounting static files: {str(e)}")
    logger.error(traceback.format_exc())

@app.get("/")
async def root():
    """Serve the index.html file"""
    try:
        return FileResponse("public/index.html")
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error serving static files")

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000, description="The chat message")
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    # Always return JSON response
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "api_key_configured": bool(OPENROUTER_API_KEY),
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "AI Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "/": "Frontend interface",
            "/health": "Health check endpoint",
            "/api/chat": "Chat endpoint (POST only)"
        },
        "documentation": "API documentation available at /docs"
    }

@app.options("/api/chat")
async def api_chat_options():
    """Handle CORS preflight for api/chat endpoint."""
    return {"message": "OK"}

@app.get("/api/chat")
async def api_chat_get():
    """Handle GET requests to /api/chat."""
    return {"message": "Please use POST method for chat requests"}

@app.post("/api/chat")
async def api_chat(message: ChatMessage, request: Request):
    """Handle chat messages with streaming response through the /api/chat endpoint."""
    try:
        logger.info(f"Received chat message: {message.message[:50]}...")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        if not OPENROUTER_API_KEY:
            logger.error("OpenRouter API key not configured")
            return JSONResponse(
                status_code=503,
                content={
                    "status": "error",
                    "message": "Service unavailable: OpenRouter API key not configured",
                    "detail": "The OpenRouter API key is missing from the environment variables"
                }
            )
        
        async def generate_response():
            try:
                logger.info(f"Connecting to OpenRouter API with model: {MODEL}")
                
                # Send start signal immediately
                yield f"data: {json.dumps({'type': 'start'})}\n\n"
                
                # Create timeout with longer duration for Vercel
                timeout = aiohttp.ClientTimeout(total=58, connect=10)
                connector = aiohttp.TCPConnector(limit=10, limit_per_host=10)
                
                async with aiohttp.ClientSession(
                    timeout=timeout, 
                    connector=connector,
                    headers={"User-Agent": "AI-Chatbot/2.0"}
                ) as session:
                    
                    headers = {
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": request.headers.get("origin", "http://localhost:8000"),
                        "X-Title": "AI Chatbot",
                        "User-Agent": "AI-Chatbot/2.0"
                    }
                    
                    payload = {
                        "model": MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are a helpful and friendly AI assistant. Follow these guidelines:
                                1. Match response length to query complexity:
                                   - Simple greetings: Brief, friendly response with 😊
                                   - Basic questions: Concise, direct answers
                                   - Complex topics: Very detailed, comprehensive responses with:
                                     * Extensive historical context
                                     * Multiple examples and case studies
                                     * Detailed explanations of theories
                                     * Statistical data and research findings
                                     * Expert opinions and quotes
                                     * Cultural and social impact
                                2. For simple interactions:
                                   - Keep responses short and friendly
                                   - Use 😊 for greetings and positive responses
                                   - Focus on being helpful and clear
                                3. For complex topics, structure with:
                                   - Clear headings for main points
                                   - Detailed bullet points with sub-points
                                   - Numbered lists with explanations
                                   - Code blocks for technical content
                                   - Tables for comparative data
                                   - Blockquotes for important quotes
                                4. Use markdown formatting:
                                   - **bold** for emphasis
                                   - *italics* for titles
                                   - `code` for technical terms
                                   - > for important quotes
                                5. Use emojis naturally:
                                   - 😊 For friendly greetings
                                   - 💡 For key insights
                                   - ⚡ For important points
                                   - ✅ For verified facts
                                   - ❤️ For expressing care
                                6. Maintain a friendly and professional tone
                                7. End responses with a friendly note or smile 😊"""
                            },
                            {"role": "user", "content": message.message}
                        ],
                        "max_tokens": MAX_TOKENS,
                        "temperature": TEMPERATURE,
                        "stream": True,
                        "presence_penalty": 0.3,
                        "frequency_penalty": 0.3,
                        "top_p": 0.95
                    }
                    
                    logger.info(f"Sending request to OpenRouter...")
                    
                    try:
                        async with session.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=payload
                        ) as response:
                            
                            logger.info(f"OpenRouter API response status: {response.status}")
                            
                            if response.status != 200:
                                error_text = await response.text()
                                logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                                
                                error_message = "Service temporarily unavailable"
                                error_detail = error_text
                                
                                if response.status == 401:
                                    error_message = "Authentication failed - invalid API key"
                                    error_detail = f"Authentication failed. API Key: {OPENROUTER_API_KEY[:8]}..."
                                    logger.error(error_detail)
                                elif response.status == 429:
                                    error_message = "Rate limit exceeded. Please try again later."
                                    error_detail = "The OpenRouter API rate limit has been exceeded"
                                
                                error_response = {
                                    "status": "error",
                                    "message": error_message,
                                    "detail": error_detail
                                }
                                logger.error(f"Sending error response: {error_response}")
                                yield f"data: {json.dumps(error_response)}\n\n"
                                return

                            # Process streaming response
                            accumulated_content = ""
                            content_received = False
                            
                            try:
                                async for line in response.content:
                                    if not line:
                                        continue
                                    
                                    line_str = line.decode('utf-8', errors='ignore').strip()
                                    
                                    # Skip empty lines
                                    if not line_str:
                                        continue
                                    
                                    # Process data lines
                                    if line_str.startswith('data: '):
                                        data_content = line_str[6:].strip()
                                        
                                        if data_content == '[DONE]':
                                            logger.info("Received [DONE] signal from OpenRouter")
                                            break
                                        
                                        try:
                                            data = json.loads(data_content)
                                            
                                            # Check for errors in the response
                                            if 'error' in data:
                                                error_msg = data['error'].get('message', 'Unknown error')
                                                yield f"data: {json.dumps({'status': 'error', 'message': error_msg})}\n\n"
                                                return
                                            
                                            # Process content
                                            if 'choices' in data and len(data['choices']) > 0:
                                                choice = data['choices'][0]
                                                delta = choice.get('delta', {})
                                                content = delta.get('content', '')
                                                
                                                if content:
                                                    content_received = True
                                                    accumulated_content += content
                                                    
                                                    # Send incremental content update
                                                    yield f"data: {json.dumps({'type': 'content', 'content': accumulated_content})}\n\n"
                                                
                                                # Check if finished
                                                finish_reason = choice.get('finish_reason')
                                                if finish_reason:
                                                    logger.info(f"Stream finished with reason: {finish_reason}")
                                                    break
                                                    
                                        except json.JSONDecodeError as e:
                                            logger.warning(f"JSON decode error: {e} for content: {data_content}")
                                            continue
                                        except Exception as e:
                                            logger.error(f"Error processing response data: {e}")
                                            logger.error(traceback.format_exc())
                                            continue
                            
                            except Exception as e:
                                logger.error(f"Error reading response stream: {e}")
                                logger.error(traceback.format_exc())
                                error_response = {
                                    "status": "error",
                                    "message": "Error reading response stream",
                                    "detail": str(e)
                                }
                                yield f"data: {json.dumps(error_response)}\n\n"
                                return
                            
                            # Send completion signal if content was received
                            if content_received and accumulated_content.strip():
                                yield f"data: {json.dumps({'type': 'complete', 'content': accumulated_content})}\n\n"
                            else:
                                # If no content was received, send an error
                                error_response = {
                                    "status": "error",
                                    "message": "No response content received",
                                    "detail": "The AI model did not generate any content"
                                }
                                yield f"data: {json.dumps(error_response)}\n\n"
                            
                    except aiohttp.ClientError as e:
                        logger.error(f"HTTP client error: {e}")
                        logger.error(traceback.format_exc())
                        error_response = {
                            "status": "error",
                            "message": "Network connection error",
                            "detail": str(e)
                        }
                        yield f"data: {json.dumps(error_response)}\n\n"
                        return
                        
            except asyncio.TimeoutError:
                logger.error("Request timeout")
                logger.error(traceback.format_exc())
                error_response = {
                    "status": "error",
                    "message": "Request timeout - please try again",
                    "detail": "The request took too long to complete"
                }
                yield f"data: {json.dumps(error_response)}\n\n"
            except Exception as e:
                logger.error(f"Unexpected error in chat endpoint: {e}")
                logger.error(traceback.format_exc())
                error_response = {
                    "status": "error",
                    "message": "An unexpected error occurred",
                    "detail": str(e)
                }
                yield f"data: {json.dumps(error_response)}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true"
            }
        )
    except Exception as e:
        logger.error(f"Top-level error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error",
                "detail": str(e)
            }
        )