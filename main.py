from fastapi import FastAPI, Request
import logging
import os
import httpx

app = FastAPI()

logging.basicConfig(level=logging.INFO)

BITRIX_WEBHOOK = os.getenv("BITRIX_WEBHOOK")  
# пример:
# https://yourdomain.bitrix24.ru/rest/1/xxxxxxxxxx/

@app.post("/")
async def bitrix_webhook(request: Request):
    data = await request.json()
    logging.info(data)

    event = data.get("event")
    payload = data.get("data", {})

    # сообщение от врача
    if event == "OnImMessageAdd":
        chat_id = payload.get("CHAT_ID")
        text = payload.get("MESSAGE")

        # минимальный автоответ оператору
        await send_to_bitrix(chat_id, f"📩 Сообщение от врача:\n{text}")

    return {"result": "ok"}


async def send_to_bitrix(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BITRIX_WEBHOOK}imbot.message.add",
            json={
                "CHAT_ID": chat_id,
                "MESSAGE": text
            }
        )
