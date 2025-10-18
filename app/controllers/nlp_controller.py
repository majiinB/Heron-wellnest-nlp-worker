from app.repositories.journal_repository import get_journal_by_id, update_journal_wellness_state
from app.services.nlp_service import NLPService
from app.utils.logger_util import logger
from app.utils.crypto_utils import decrypt
from app.config.env_config import env
import asyncio

class NLPcontroller:
    def __init__(self, nlp_service: NLPService):
        self.nlp_service = nlp_service
        self.model_lock = asyncio.Lock()

    async def process_pubsub_payload(self, payload):
        # Extract relevant info from payload
        event_type = payload.get("eventType", "")
        user_id = payload.get("userId", "")
        journal_id = payload.get("journalId", "")

        if event_type != "JOURNAL_ENTRY_CREATED":
            logger.info(f"Ignoring event type: {event_type}")
            return None

        # Fetch encrypted journal content from DB
        encrypted_content = await get_journal_by_id(journal_id, user_id)
        if not encrypted_content:
            logger.warning(f"No journal entry found for journal_id={journal_id}, user_id={user_id}")
            return None

        # Decrypt journal content
        decrypted_content = decrypt(
            encrypted=encrypted_content,
            secret=env.CONTENT_ENCRYPTION_KEY
        )

        async with self.model_lock:
            # Analyze text using NLP model
            preds = self.nlp_service.analyze_text(decrypted_content)

        # Update journal entry with mood analysis
        await update_journal_wellness_state(journal_id, user_id, preds)
        logger.info(f"Updated mood for journal {journal_id}")
        return preds