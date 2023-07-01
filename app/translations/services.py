from dataclasses import dataclass
from typing import TYPE_CHECKING

from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind


if TYPE_CHECKING:
    from returns.result import Result
    from google.cloud.translate_v2 import Client as TranslateClient
    from app.translations.types import TranslateClientTranslateResponse


@dataclass
class TranslatePayload:
    text: str
    source_locale: str
    target_locale: str


class TranslationService:
    client: "TranslateClient"

    def __init__(self, client: "TranslateClient") -> None:
        self.client = client

    def translate(
        self, text: str, source_locale: str, target_locale: str
    ) -> "Result[str, Exception]":
        return flow(
            TranslatePayload(
                text=text,
                source_locale=source_locale,
                target_locale=target_locale,
            ),
            self.__translate,
            bind(self.__get_translated_text_from_translate_client_translate_response),
        )

    @safe
    def __translate(
        self, payload: TranslatePayload
    ) -> "TranslateClientTranslateResponse":
        return self.client.translate(
            values=payload.text,
            target_language=payload.target_locale,
            source_language=payload.source_locale,
        )

    @safe
    def __get_translated_text_from_translate_client_translate_response(
        self,
        response: "TranslateClientTranslateResponse",
    ) -> str:
        return response["translatedText"]
