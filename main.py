from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from translate import translate_text
import os



GLOBAL_TOKEN = os.getenv('GLOBAL_TOKEN')

# Supported language codes for validation
SUPPORTED_LANGUAGES = {
    "en": "English",
    "th": "Thai",
    "zh": "Chinese",
    "fr": "French",
    "ar": "Arabic",
    "ja": "Japanese",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ru": "Russian"
}
app = FastAPI(
    title="Khain | Rapid Translate API",
    description="API service for fast language translation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

security = HTTPBearer()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "Hello from Khain | Rapid Translate API!"}
    )

# Authentication dependency
async def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not GLOBAL_TOKEN:
        raise HTTPException(status_code=500, detail="Server authentication not configured")
    if token != GLOBAL_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return token

def validate_language_code(lang_code: str) -> str:
    """Validate that the language code is supported"""
    if lang_code not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400, 
            detail=f"Language code '{lang_code}' not supported. Supported languages: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        )
    return lang_code

@app.get("/translate")
async def translate(
    request: Request,
    text: str,
    lang: str = "en",
    to: str = "th",
    # token: str = Depends(get_current_token)
):
    """
    Translate text between languages
    
    Parameters:
    - text: The text to translate (required)
    - lang: Source language code (default: 'en')
    - to: Target language code (default: 'th')
    - Authorization: Bearer token (required in header)
    """
    # Validate inputs
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Validate language codes
    source_lang = validate_language_code(lang)
    target_lang = validate_language_code(to)
    
    try:
  
        translator = translate_text(source_lang, target_lang, text)
        
      
        
        return {
            "original_text": text,
            "translated_text": translator,
            "source_language": source_lang,
            "target_language": target_lang,
        }
    except ValueError as e:
        # Handle specific translation errors
        raise HTTPException(status_code=400, detail=f"Translation error: {str(e)}")
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "translation-api"}

# Documentation endpoint
@app.get("/api-info")
async def api_info():
    return {
        "name": "Khain Rapid Translate API",
        "version": "1.0.0",
        "supported_languages": SUPPORTED_LANGUAGES
    }