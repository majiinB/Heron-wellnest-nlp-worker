import asyncio

from fastapi import APIRouter, Request
from app.config.env_config import env
from app.services.nlp_service import NLPService
from app.utils.logger_util import logger
from app.controllers.nlp_controller import NLPcontroller
import base64
import json
import asyncio

router = APIRouter()

# Define label mapping
id_to_label = {
        0: "L1", # Anxiety
        1: "L2", # Normal
        2: "L3", # Depression
        3: "L4", # Suicidal
        4: "L5" # Stress
    }

# Load NLP model once at startup
nlp_service = NLPService(model_path=env.MODEL_PATH, id_to_label=id_to_label)
nlp_controller = NLPcontroller(nlp_service)

model_lock = asyncio.Lock()

@router.post("/pubsub")
async def receive_pubsub(request: Request):
    try:
        envelope = await request.json()
        if not envelope or "message" not in envelope:
            logger.error("Invalid Pub/Sub message format")
            return {"error": "Bad Request"}, 400

        if "message" not in envelope:
            logger.error("No message field in Pub/Sub message")
            return {"error": "Bad Request"}, 400

        pubsub_message = envelope["message"]

        if "data" not in pubsub_message:
            logger.error("No data field in Pub/Sub message")
            return {"error": "Bad Request"}, 400

        # Decode the Pub/Sub message data
        data_str = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        payload = json.loads(data_str)

        await nlp_controller.process_pubsub_payload(payload)

        return {"", 204}
    except Exception as e:
        logger.error(f"Error processing Pub/Sub message: {e}")
        # Return non-2xx so Pub/Sub retries the message
        return {"error": str(e)}, 500

