from http.client import INTERNAL_SERVER_ERROR
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from returns.result import Success

from app.translations.dependencies import get_translation_service
from app.translations.models import TranslationPayload, TranslationResponse


if TYPE_CHECKING:
    from app.translations.services import TranslationService


router = APIRouter(tags=["translations"], prefix="/translations")


@router.post("")
def translate(
    payload: TranslationPayload,
    translation_service: Annotated[
        "TranslationService", Depends(get_translation_service)
    ],
) -> TranslationResponse:
    translate_result = translation_service.translate(
        text=payload.text,
        source_locale=payload.source_locale,
        target_locale=payload.target_locale,
    )
    match translate_result:
        case Success(translated_text):
            return TranslationResponse(translated_text=translated_text)
        case _:
            raise HTTPException(
                status_code=INTERNAL_SERVER_ERROR, detail="Something went wrong"
            )
