from fastapi import FastAPI, Request 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

GLOBAL_TOKEN = os.getenv('GLOBAL_TOKEN')

app = FastAPI()
security = HTTPBearer()
templates = Jinja2Templates(directory="templates")  # Create a `templates` folder

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",  # File in `templates/` folder
        {"request": request, "message": "Hello from Khain | Rapid Translate API!"}
    )


# Authentication dependency
async def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Add your token validation logic here
    if token != GLOBAL_TOKEN:  # Replace with your actual token validation
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/translate")
async def translate(
    request: Request,
    text: str,
    lang: str = "en",  # Default source language
    to: str = "th",    # Default target language
    token: str = Depends(get_current_token)  # Requires Bearer token
):
    """
    Translate text between languages
    
    Parameters:
    - text: The text to translate (required)
    - lang: Source language code (default: 'en')
    - to: Target language code (default: 'th')
    - Authorization: Bearer token (required)
    """
    from pythainlp.translate import Translate
    try:
        # Initialize translator
        translator = Translate(lang, to, engine="small")  # or "large" for fairseq
        
        # Perform translation
        translation = translator.translate(text)
        
        return {
            "original_text": text,
            "translated_text": translation,
            "source_language": lang,
            "target_language": to
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))