import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from lingua import Language, LanguageDetectorBuilder
from datetime import datetime

app = FastAPI()

security = HTTPBearer()
API_TOKEN = os.environ.get("API_TOKEN")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not API_TOKEN:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="API_TOKEN not configured")
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

languages = [
    Language.CHINESE,
    Language.ENGLISH,
    Language.JAPANESE,
    Language.KOREAN,
    Language.FRENCH,
    Language.GERMAN,
    Language.SPANISH,
    Language.RUSSIAN,
    Language.PORTUGUESE,
    Language.ARABIC,
    Language.HINDI,
    Language.ITALIAN,
    Language.TURKISH,
    Language.DUTCH,
    Language.POLISH,
    Language.UKRAINIAN,
    Language.VIETNAMESE,
    Language.INDONESIAN,
    Language.THAI,
    Language.HEBREW,
    Language.BRAZILIAN_PORTUGUESE,
]

detector = LanguageDetectorBuilder.from_languages(*languages).build()

class TextRequest(BaseModel):
    text: str

@app.get("/health")
async def status_check():
    return {
        "code": 0,
        "data": {
            "status": "UP",
            "time": datetime.utcnow().isoformat()
        },
        "message": "ok"
    }

@app.post("/detect")
def detect_language(request: TextRequest, token: str = Depends(verify_token)):
    if not request.text or not request.text.strip():
        return {"language": None}
    language = detector.detect_language_of(request.text)
    if language is None:
        return {"language": None}
    return {"language": language.iso_code_639_1.name.lower()}
