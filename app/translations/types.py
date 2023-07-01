from typing import TypedDict


class TranslateClientSupportedLocale(TypedDict):
    language: str
    name: str


TranslateClientSupportedLocalesResponse = list[TranslateClientSupportedLocale]


class TranslateClientTranslateResponse(TypedDict):
    translatedText: str
    input: str
