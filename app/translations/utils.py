from http.client import INTERNAL_SERVER_ERROR
from typing import Callable, TypeVar
from fastapi import HTTPException

from returns.result import Success, Failure, Result
from google.api_core.exceptions import ClientError

ResultSuccessVar = TypeVar("ResultSuccessVar")
ResultMappingVar = TypeVar("ResultMappingVar")


def handle_translation_service_result(
    result: Result[ResultSuccessVar, Exception],
    map_callback: Callable[[ResultSuccessVar], ResultMappingVar],
) -> ResultMappingVar:
    match result:
        case Success(success):
            return map_callback(success)
        case Failure(failure):
            match failure:
                case KeyError():
                    raise HTTPException(
                        status_code=INTERNAL_SERVER_ERROR, detail="Something went wrong"
                    )
                case ClientError():
                    raise HTTPException(
                        status_code=getattr(failure, "code", None)
                        or INTERNAL_SERVER_ERROR,
                        detail=getattr(failure, "message", None)
                        or "Something went wrong",
                    )

    raise HTTPException(
        status_code=INTERNAL_SERVER_ERROR, detail="Something went wrong"
    )
