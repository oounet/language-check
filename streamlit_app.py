import streamlit as st
from lingua import Language, LanguageDetectorBuilder

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

st.title("语言检测")

text = st.text_area("请输入文本")

if st.button("检测语言"):
    if not text.strip():
        st.warning("请输入文本")
    else:
        language = detector.detect_language_of(text)

        if language:
            confidence = detector.compute_language_confidence(
                text,
                language
            )

            st.success(
                f"语言：{language.name}\n\n"
                f"置信度：{confidence:.4f}"
            )
        else:
            st.warning("无法识别语言")
