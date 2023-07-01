from typing import TYPE_CHECKING, Annotated, TypedDict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.translations.dependencies import get_translate_api

if TYPE_CHECKING:
    from google.cloud.translate_v2 import Client as TranslateClient


router = APIRouter(tags=["translations"], prefix="/translations")


class TranslationPayload(BaseModel):
    text: str
    source_locale: str
    target_locale: str


class TranslationResponse(BaseModel):
    translated_text: str


class TranslateClientTranslateResponse(TypedDict):
    translatedText: str
    input: str


@router.post("")
def translate(
    payload: TranslationPayload,
    translation_client: Annotated["TranslateClient", Depends(get_translate_api)],
) -> TranslationResponse:
    try:
        translation: TranslateClientTranslateResponse = translation_client.translate(
            values=payload.text,
            target_language=payload.target_locale,
            source_language=payload.source_locale,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return TranslationResponse(translated_text=translation["translatedText"])
