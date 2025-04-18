from typing import List, Optional
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from pydantic import HttpUrl, BaseModel
from random import randint

from crud import create_screenshot_run, get_screenshots_for_run
from database import get_db
from tasks import run_collector_task

# Instantiate the Fastapi app
app = FastAPI(title="Collector Service")


# Pydantic schemas for request bodies and api responses
class CaptureScreenshotRequest(BaseModel):
    start_url: HttpUrl
    n_links: int


class CaptureScreenshotResponse(BaseModel):
    run_id: str


# TODO: add a run status field that is managed during the selenium step
class ReturnScreenshotResponse(BaseModel):
    run_id: str
    screenshots: Optional[List[str]]


class StatusResponse(BaseModel):
    status: str


@app.get("/isalive", response_model=StatusResponse)
async def is_alive():
    return StatusResponse(status="alive")


# TODO: improve response and handling for wrong urls, or other issues.
@app.post(
    "/screenshots",
    response_model=CaptureScreenshotResponse,
    status_code=202,
)
async def capture_screenshots(
    request: CaptureScreenshotRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    # TODO: use uuid for example to generate run_ids
    # Perfectly aware this is not a robust solution
    # I chose this for simplicity to have a simple input for the GET route
    run_id = str(randint(1000, 9999))  # casting str to mimic a uuid type

    # Create the run record in the database
    try:
        create_screenshot_run(
            db=db,
            run_id=run_id,
            start_url=str(request.start_url)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error creating run: {e}")

    # Add the Selenium task to background processing
    background_tasks.add_task(
        run_collector_task,
        run_id=run_id,
        start_url=str(request.start_url),
        num_links=request.n_links
    )

    return CaptureScreenshotResponse(run_id=run_id)


@app.get(
    "/screenshots/{run_id}",
    response_model=ReturnScreenshotResponse,
)
async def return_screenshots(
    run_id,
    db=Depends(get_db)
):
    # Fetch screenshot records associated with the run_id
    # TODO: move storage to shared location so that returned uri's can be accessible by client
    db_screenshots = get_screenshots_for_run(db=db, run_id=run_id)
    filepaths = [s.filepath for s in db_screenshots] if db_screenshots else None

    if not filepaths:
        raise HTTPException(status_code=404, detail=f"{run_id} either is invalid, or has no screenshots... ask your dev to add run_status that he put off so many times")

    return ReturnScreenshotResponse(
        run_id=run_id,
        screenshots=filepaths
    )
