import json
import time

import jwt
from fastapi import FastAPI

app = FastAPI()


config = json.load(open("/centrifugo/config.json"))


@app.get("/")
def home():
    return {}


@app.get("/get_token")
def get_token():
    claims = {"sub": "something", "exp": int(time.time()) + 24 * 3600}

    secret_key = config["token_hmac_secret_key"]

    token = jwt.encode(claims, secret_key, algorithm="HS256")
    return {"token": token}
