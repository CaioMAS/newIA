from fastapi import FastAPI # type: ignore
from app.routes import sinais
import asyncio
from app.services.coleta import iniciar_coleta

app = FastAPI()

@app.on_event("startup")
async def start_tasks():
    asyncio.create_task(iniciar_coleta())

app.include_router(sinais.router)
