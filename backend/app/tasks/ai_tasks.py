from app.tasks.celery_app import celery_app
from app.modules.ai.embeddings.service import embed_text
from app.modules.ai.embeddings.pinecone_client import upsert_vectors, delete_vectors_by_ids


@celery_app.task
def embed_menu_item(item_id: str, restaurant_id: str, text: str):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        vector = loop.run_until_complete(embed_text(text))
        loop.run_until_complete(upsert_vectors(
            restaurant_id,
            [{"id": f"menu_{item_id}", "values": vector, "metadata": {"text": text, "type": "menu_item", "item_id": item_id}}],
        ))
    finally:
        loop.close()
    return f"Embedded menu item {item_id}"


@celery_app.task
def delete_menu_item_embedding(item_id: str, restaurant_id: str):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(delete_vectors_by_ids(restaurant_id, [f"menu_{item_id}"]))
    finally:
        loop.close()
    return f"Deleted embedding for menu item {item_id}"


@celery_app.task
def embed_knowledge_chunk(chunk_id: str, restaurant_id: str, text: str):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        vector = loop.run_until_complete(embed_text(text))
        loop.run_until_complete(upsert_vectors(
            restaurant_id,
            [{"id": f"kb_{chunk_id}", "values": vector, "metadata": {"text": text, "type": "knowledge_base", "chunk_id": chunk_id}}],
        ))
    finally:
        loop.close()
    return f"Embedded knowledge chunk {chunk_id}"


@celery_app.task
def process_menu_bulk_upload(file_path: str, restaurant_id: str):
    return f"Processing bulk upload for restaurant {restaurant_id}"
