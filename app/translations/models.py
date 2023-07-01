from pydantic import BaseModel


class SupportedLocalesResponse(BaseModel):
    language: str
    name: str


class TranslationPayload(BaseModel):
    text: str
    source_locale: str
    target_locale: str


class TranslationResponse(BaseModel):
    translated_text: str
