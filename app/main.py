from fastapi import FastAPI

app = FastAPI(title="Collector Service")

@app.get("/isalive")
async def is_alive():
  return {"status": "alive"}
