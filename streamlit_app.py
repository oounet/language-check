from fastapi import FastAPI
from pydantic import BaseModel
from lingua import Language, LanguageDetectorBuilder

app = FastAPI(
    title="Language Detection API",
    version="1.0.0"
)

# 支持的语言
languages = [
    Language.CHINESE,
    Language.ENGLISH,
    Language.JAPANESE,
    Language.KOREAN,
    Language.FRENCH,
    Language.GERMAN,
    Language.SPANISH,
    Language.ITALIAN,
    Language.PORTUGUESE,
    Language.RUSSIAN,
]

# 创建检测器
detector = LanguageDetectorBuilder.from_languages(*languages).build()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "message": "Language Detection API is running"
    }


@app.post("/detect")
def detect_language(request: TextRequest):
    text = request.text.strip()

    if not text:
        return {
            "language": None,
            "confidence": 0,
            "message": "text cannot be empty"
        }

    language = detector.detect_language_of(text)

    if language is None:
        return {
            "language": None,
            "confidence": 0
        }

    # Lingua 获取置信度
    confidence = detector.compute_language_confidence(text, language)

    return {
        "language": language.name,
        "confidence": round(confidence, 4)
    }
