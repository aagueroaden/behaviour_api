from app.behaviour.module import behaviour_module
from app.mvp_logging.module import mvp_log_module
from app.behaviour import models
from app.behaviour_db import engine
from app.sentry import initialize_sentry
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
# from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        # Startup code: Create tables when the application starts
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        logging.error(f"Failed to create/initialize tables: {str(e)}")
        sys.exit(1)
    try:
        initialize_sentry()
    except Exception as e:
        logging.error(f"Error initialize sentry: {str(e)}")

    yield  # Control is passed to the app here

    logging.info("SHUTTING DOWN: DISPOSING ENGINE")

    engine.dispose()


app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # this should change to certain domains only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the behaviour module
app.include_router(behaviour_module)
app.include_router(mvp_log_module)

# Instrumentator().instrument(app).expose(app)


# generic endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Behaviour API"}
