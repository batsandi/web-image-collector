from fastapi import FastAPI
from pydantic import HttpUrl
app = FastAPI(title="Collector Service")


@app.get("/isalive")
async def is_alive():
    return {"status": "alive"}


@app.post("/screenshots")
async def capture_screenshots(start_url: HttpUrl, n_links: int):
    return {"status": f"{str(start_url)}"}


@app.get("/screenshot/{run_id}")
async def return_screenshots(run_id: str):
    return {"status": f"Screenshot for run ID {run_id}"}
