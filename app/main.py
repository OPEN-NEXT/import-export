from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import manifests

import uvicorn
import os

app = FastAPI()
app.include_router(manifests.router)

TMP_FOLDER = "/tmp/outputs/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if the /tmp/outputs folder exists
try:
    if not os.path.exists(TMP_FOLDER):
        print("Creating tmp folder")
        os.makedirs(TMP_FOLDER)

except Exception as e:
    print(e)

if(__name__ == "__main__"):

    uvicorn.run(app, host="0.0.0.0", port=8000)