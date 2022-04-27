import json
import time

import jwt
from cent import Client
from fastapi import FastAPI, Request
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
CENTRIFUGO_URL = "http://localhost:8000"


@app.get("/")
async def home():
    return {}


@app.get("/get_token")
async def get_token():
    claims = {"sub": "something", "exp": int(time.time()) + 24 * 3600}
    token = jwt.encode(claims, CENTRIFUGO_SECRET, algorithm="HS256")
    return {"token": token}


@app.post("/send_message")
async def send_message(request: Request):
    """Sends message to test-channel"""
    data = await request.json()

    channel = "news"

    msg = {
        "custom_key1": "news",
        "custom_key2": data.get("anything", ""),
        "custom_key3": "custom value 3",
        "custom_key4": "custom value 4",
    }

    client = Client(CENTRIFUGO_URL, api_key=CENTRIFUGO_API_KEY, timeout=3)
    client.publish(channel, msg)

    return {"success": "ok"}
