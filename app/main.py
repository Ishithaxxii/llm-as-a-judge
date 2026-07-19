from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="LLM as a Judge",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "LLM as a Judge API Running"}
