from fastapi import APIRouter, Request
from app.config.env_config import env
from app.services.nlp_service import NLPService
import base64

router = APIRouter()

# Load NLP model once at startup
nlp_service = NLPService(env.MODEL_PATH)
#
from torch.onnx import export


@router.post("/")
async def receive_pubsub(request: Request):
    # envelope = await request.json()
    # if not envelope or "message" not in envelope:
    #     return {"error": "Invalid Pub/Sub message format"}
    #
    # pubsub_message = envelope["message"]
    # data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
    #
    # # Run prediction
    preds = nlp_service.analyze_text("Hello, world!")
    print(f"Prediction: {preds}")

    return # {"prediction": preds}

