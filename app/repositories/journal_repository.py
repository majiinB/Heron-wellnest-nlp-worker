from app.utils.db_utils import fetch_one, fetch_all, execute_query
import json

async def get_journal_by_id(journal_id: str, user_id: str):
    print(f"📥 Fetching journal {journal_id} for user {user_id}")
    query = "SELECT content_encrypted FROM journal_entries WHERE journal_id = :journal_id AND user_id = :user_id"
    params = {"journal_id": journal_id, "user_id": user_id}
    rows = await fetch_all(query, params)

    if not rows:
        raise ValueError("Journal entry not found")

    row = rows[0]
    print(f"📤 Query returned rows: {rows}")

    if not rows:
        print("❌ No journal entry found!")
        raise ValueError("Journal entry not found")

    # handle both dict or tuple row formats
    encrypted_content = rows[0]["content_encrypted"]
    print(f"🧩 Encrypted content fetched: {encrypted_content}")
    return encrypted_content

async def update_journal_wellness_state(journal_id: str, user_id: str, wellness_state: dict):
    query = """
        UPDATE journal_entries
        SET wellness_state = :wellness_state
        WHERE journal_id = :journal_id AND user_id = :user_id
    """
    params = {
        "journal_id": journal_id,
        "user_id": user_id,
        "wellness_state": json.dumps(wellness_state)
    }
    await execute_query(query, params)
