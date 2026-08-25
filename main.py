from fastapi import FastAPI
from pydantic import BaseModel
from lingua import Language, LanguageDetectorBuilder

app = FastAPI(title="Language Detection API")


# 支持的语言
languages = [
    Language.CHINESE,
    Language.ENGLISH,
    Language.JAPANESE,
    Language.KOREAN,
    Language.FRENCH,
    Language.GERMAN,
    Language.SPANISH,
]

# 创建语言检测器
detector = LanguageDetectorBuilder.from_languages(*languages).build()


class TextRequest(BaseModel):
    text: str


class LanguageResponse(BaseModel):
    text: str
    language: str
    language_code: str


@app.post("/detect", response_model=LanguageResponse)
def detect_language(request: TextRequest):
    language = detector.detect_language_of(request.text)

    if language is None:
        return {
            "text": request.text,
            "language": "UNKNOWN",
            "language_code": "unknown",
        }

    return {
        "text": request.text,
        "language": language.name,
        "language_code": language.iso_code_639_1.name.lower(),
    }
