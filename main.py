import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BITRIX_REST_URL = os.getenv("BITRIX_REST_URL")
BOT_ID = os.getenv("BOT_ID")


@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    print("INCOMING:", data)

    if data.get("event") != "ONIMBOTMESSAGEADD":
        return {"status": "ignored"}

    payload = data.get("data", {})
    author_id = str(payload.get("AUTHOR_ID"))
    dialog_id = payload.get("DIALOG_ID")
    message = payload.get("MESSAGE", "")

    # оператор → игнор
    if author_id != "0":
        return {"status": "operator_ignored"}

    send_message(dialog_id, f"Эхо: {message}")
    return {"status": "ok"}


def send_message(dialog_id: str, text: str):
    url = f"{BITRIX_REST_URL}/imbot.message.add"
    requests.post(url, json={
        "BOT_ID": BOT_ID,
        "DIALOG_ID": dialog_id,
        "MESSAGE": text
    })
