from fastapi import FastAPI

from app.translations.router import router as translations_router

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}


app.include_router(translations_router)
