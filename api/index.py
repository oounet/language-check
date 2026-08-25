from fastapi import FastAPI
from pydantic import BaseModel
from lingua import Language, LanguageDetectorBuilder

app = FastAPI()


languages = [
    Language.CHINESE,
    Language.ENGLISH,
    Language.JAPANESE,
    Language.KOREAN,
    Language.FRENCH,
    Language.GERMAN,
    Language.SPANISH,
]

detector = LanguageDetectorBuilder.from_languages(*languages).build()


class TextRequest(BaseModel):
    text: str


@app.post("/detect")
def detect_language(request: TextRequest):
    language = detector.detect_language_of(request.text)

    if language is None:
        return {
            "language": "unknown"
        }

    return {
        "language": language.iso_code_639_1.name.lower()
    }
