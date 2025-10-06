from fastapi import FastAPI
from app.routes.nlp_route import router
from app.worker import start_worker
from app.config.env_config import env

app = FastAPI(title="NLP Worker")

app.include_router(router)

if(env.ENVIRONMENT != "production"):
    @app.on_event("startup")
    async def startup_event():
        import threading
        thread = threading.Thread(target=start_worker, daemon=True)
        thread.start()
        print("✅ Pub/Sub worker started in background") 