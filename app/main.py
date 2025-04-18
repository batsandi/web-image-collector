from typing import List, Optional
from fastapi import FastAPI
from pydantic import HttpUrl, BaseModel
from random import randint

app = FastAPI(title="Collector Service")


class CaptureScreenshotRequest(BaseModel):
    start_url: HttpUrl
    n_links: int


class CaptureScreenshotResponse(BaseModel):
    run_id: str


class ReturnScreenshotResponse(BaseModel):
    run_id: str
    status: str
    screenshots: Optional[List[str]]


class StatusResponse(BaseModel):
    status: str


@app.get("/isalive")
async def is_alive():
    return {"status": "alive"}


@app.post("/screenshots")
async def capture_screenshots(start_url: HttpUrl, n_links: int):
    # TODO: use uuid for example to generate run_ids
    # Perfectly aware this is not a robust solution
    # I chose this for simplicity to have a simple input for the GET route
    run_id = randint(1000, 9999)

    return {"run_id": f"{run_id}"}


@app.get("/screenshot/{run_id}")
async def return_screenshots(run_id: str):
    return {"screenshots": ['list of screenshots']}
