from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from google.cloud.translate_v2 import Client as TranslateClient

from app.dependencies.env import get_env
from app.translations.services import TranslationService

if TYPE_CHECKING:
    from app.dependencies.env import Env


def __get_translate_api(env: Annotated["Env", Depends(get_env)]) -> TranslateClient:
    return TranslateClient(
        client_options={
            "api_key": env["translate_api_key"],
            "quota_project_id": env["gcp_project_id"],
        }
    )


def get_translation_service(
    translation_client: Annotated["TranslateClient", Depends(__get_translate_api)]
):
    return TranslationService(client=translation_client)
