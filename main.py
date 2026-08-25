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

# 只加载需要的语言，并开启低精度模式进一步减内存（短文本准确率会下降一点）
detector = (
    LanguageDetectorBuilder.from_languages(*languages)
    .with_low_accuracy_mode()   # 可选，显著降低内存
    .build()
)

class TextRequest(BaseModel):
    text: str

@app.post("/detect")
def detect_language(request: TextRequest):
    language = detector.detect_language_of(request.text)
    if language is None:
        return {"language": "unknown"}
    return {
        "language": language.iso_code_639_1.name.lower()
    }
