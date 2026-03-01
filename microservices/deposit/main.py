from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router
import os
import uvicorn

load_dotenv()

PORT = os.getenv("PORT")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_all_tables_async()
    # Load the ML model
    # ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean uuvicornp the ML models and release the resources
    # ml_models.clear()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "microservices.deposit.main:app",
        reload=True,
        host="0.0.0.0",
        port=int(PORT or 8005),
    )
