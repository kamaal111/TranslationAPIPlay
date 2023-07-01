from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI

from app.dependencies.translate_client import get_translate_api

if TYPE_CHECKING:
    from google.cloud.translate_v2 import Client as TranslateClient

app = FastAPI()


@app.get("/")
def read_root(
    translate_client: Annotated["TranslateClient", Depends(get_translate_api)]
):
    return translate_client.get_languages()
