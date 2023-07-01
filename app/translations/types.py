from typing import List, TypedDict


class TranslateClientSupportedLocale(TypedDict):
    language: str
    name: str


TranslateClientSupportedLocalesResponse = List[TranslateClientSupportedLocale]


class TranslateClientTranslateResponse(TypedDict):
    translatedText: str
    input: str
