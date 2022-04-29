import json
import time

import jwt
from cent import Client
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

config = json.load(open("/centrifugo/config.json"))

CENTRIFUGO_API_KEY = config["api_key"]
CENTRIFUGO_SECRET = config["token_hmac_secret_key"]
CENTRIFUGO_API_URL = "http://centrifugo:8000/api"


@app.get("/")
async def home():
    return {}


@app.get("/get_token")
async def get_token():
    claims = {
        "sub": "some_user_id_can_be_here",
        "exp": int(time.time()) + 24 * 3600,
    }
    token = jwt.encode(claims, CENTRIFUGO_SECRET, algorithm="HS256")
    return {"token": token}


@app.post("/send_message")
async def send_message(request: Request, background_tasks: BackgroundTasks):
    """Sends message to news"""
    data = await request.json()

    channel = "news"

    msg = {
        "custom_key1": data.get("anything", ""),
        "custom_key2": "custom value 2",
    }

    background_tasks.add_task(publish_task, channel, msg)
    return {"info": "message sent"}


def publish_task(channel, msg):
    client = Client(CENTRIFUGO_API_URL, api_key=CENTRIFUGO_API_KEY, timeout=3)
    client.publish(channel, msg)
