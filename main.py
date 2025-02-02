import uvicorn
from fastapi import FastAPI

from src.application.routers import router

app = FastAPI()


app.include_router(router)

# This block is only needed for local runs
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
