from fastapi import FastAPI, Request, responses, BackgroundTasks
import requests
import json
import uvicorn
from dotenv import load_dotenv
import os
from queue import Queue
import threading
from process_queue import process_queue

app = FastAPI()

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WAM_ID = os.getenv("WAM_ID")

sessions = {}
message_queue = Queue()

worker_thread = threading.Thread(target=process_queue, 
                                 args=(message_queue, sessions, WAM_ID, WHATSAPP_TOKEN), 
                                 daemon=True)
worker_thread.start()

@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook succesfully verified.")
        return responses.PlainTextResponse(challenge)
    else:
        return responses.JSONResponse(status_code=403, content={"error": "invalid token"})


# Endpoint para recibir mensajes
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    print("Message recieved:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # Verificamos si el mensaje tiene texto
    if data.get("entry"):
        changes = data["entry"][0].get("changes")
        if changes:
            value = changes[0].get("value", {})
            messages = value.get("messages")
            if messages:
                message = messages[0]
                from_number = message["from"]
                text = message["text"]["body"]

                print(f"From: {from_number} | Text: {text}")

                # Necesario al usar numero de prueba
                from_number = from_number.replace("54911", "541115")

                message_queue.put((from_number, text))

    return {"status": "EVENT_RECEIVED"} #200 ok automatico en este caso

# ▶️ Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
