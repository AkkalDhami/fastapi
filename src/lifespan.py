from contextlib import asynccontextmanager

from fastapi import FastAPI

from configs import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Connecting DB...")

    yield

    logger.info("Closing DB...")
