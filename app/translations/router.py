from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends

from app.translations.dependencies import get_translation_service
from app.translations.models import (
    SupportedLocalesResponse,
    TranslationPayload,
    TranslationResponse,
)
from app.translations.utils import handle_translation_service_result


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
    result = translation_service.translate(
        text=payload.text,
        source_locale=payload.source_locale,
        target_locale=payload.target_locale,
    )
    return handle_translation_service_result(
        result=result,
        map_callback=lambda success: TranslationResponse(translated_text=success),
    )


@router.get("/supported-locales", response_model=list[SupportedLocalesResponse])
def supported_locales(
    target: str,
    translation_service: Annotated[
        "TranslationService", Depends(get_translation_service)
    ],
):
    result = translation_service.get_supported_locales(target_locale=target)
    return handle_translation_service_result(
        result=result, map_callback=lambda success: success
    )
