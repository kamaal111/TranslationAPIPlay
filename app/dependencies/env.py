import os
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()

TRANSLATE_API_KEY = os.getenv("TRANSLATE_API_KEY")
if not TRANSLATE_API_KEY:
    raise Exception("No translate api key provided")

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
if not GCP_PROJECT_ID:
    raise Exception("No gcp project id provided")


class Env(TypedDict):
    translate_api_key: str
    gcp_project_id: str


def get_env() -> Env:
    return {"translate_api_key": TRANSLATE_API_KEY, "gcp_project_id": GCP_PROJECT_ID}
