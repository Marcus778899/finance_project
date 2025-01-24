import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .setting import LogMiddleware, send_info
from .Controller import image_router
from .TelegramBot.Initial import start_polling

async def app_lifespan(app: FastAPI):
    polling_thread = threading.Thread(target=start_polling, daemon=True)
    polling_thread.start()
    send_info("Telegram bot polling thread started.")
    yield  
    send_info("Application shutting down.")

app = FastAPI(lifespan=app_lifespan)

app.add_middleware(LogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(image_router)

@app.get("/")
async def Hello_world():
    return {"status_code":200}
