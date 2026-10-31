import os
import asyncio
import base64

import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = "Ключ от Bare API"
SITE = "http://5.42.211.111/"

GET_DELAY = 1.0
MAX_ATTEMPTS = 10


@app.post("/solve")
async def solve(file: UploadFile = File(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured")
        
    image = await file.read()

    if not image:
        raise HTTPException(status_code=400, detail="Empty image")

    if len(image) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large")

    base64_image = base64.b64encode(image).decode("utf-8")

    async with httpx.AsyncClient(timeout=15) as client:

        # Отправка изображения
        try:
            response = await client.post(
                f"{SITE}in.php",
                data={"key": API_KEY, "method": "base64", "body": base64_image},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Bare API connection error")

        if not response.text.startswith("OK|"):
            raise HTTPException(
                status_code=502, detail=f"Bare API error: {response.text}"
            )

        captcha_id = response.text.split("|", 1)[1]

        # Получение результата
        for _ in range(MAX_ATTEMPTS):

            await asyncio.sleep(GET_DELAY)

            try:
                result = await client.get(
                    f"{SITE}res.php",
                    params={"key": API_KEY, "action": "get", "id": captcha_id},
                )
            except httpx.RequestError:
                raise HTTPException(status_code=502, detail="Bare API connection error")

            if result.text.startswith("OK|"):
                answer = result.text.split("|", 1)[1]

                return {"success": True, "captcha_id": captcha_id, "result": answer}

            if result.text != "CAPCHA_NOT_READY":
                raise HTTPException(
                    status_code=502, detail=f"Bare API error: {result.text}"
                )

        return {
            "success": False,
            "captcha_id": captcha_id,
            "error": "Timeout: captcha not solved",
        }
