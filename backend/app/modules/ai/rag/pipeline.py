from typing import List, Optional, AsyncIterator
import json

from app.modules.ai.embeddings.service import embed_text
from app.modules.ai.embeddings.pinecone_client import query_vectors
from app.modules.ai.vision.service import analyze_food_image
from app.modules.ai.prompts.templates import build_system_prompt
from app.core.config import get_settings
from openai import AsyncOpenAI

settings = get_settings()
openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


async def rag_pipeline(
    restaurant_id: str,
    restaurant_name: str,
    user_message: str,
    consumer_profile: Optional[dict] = None,
    image_bytes: Optional[bytes] = None,
    conversation_history: Optional[List[dict]] = None,
) -> AsyncIterator[str]:
    vision_output = None
    if image_bytes:
        vision_output = await analyze_food_image(image_bytes)

    query_parts = [user_message]
    if vision_output:
        query_parts.append(f"[Image identified: {vision_output}]")
    if consumer_profile:
        prefs = consumer_profile.get("preferences", [])
        if prefs:
            query_parts.append(f"Preferences: {', '.join(prefs)}")
    query = " ".join(query_parts)

    query_embedding = await embed_text(query)
    vector_results = await query_vectors(restaurant_id, query_embedding, top_k=8)

    retrieved_contexts = []
    for match in vector_results:
        if match.metadata:
            text = match.metadata.get("text", "")
            score = match.score
            retrieved_contexts.append({"text": text, "score": score, "id": match.id})

    system_prompt = build_system_prompt(
        restaurant_name=restaurant_name,
        preferences=(consumer_profile or {}).get("preferences", []),
        allergies=(consumer_profile or {}).get("allergies", []),
        region=(consumer_profile or {}).get("region"),
    )

    context_block = "\n\n".join(
        [f"- {ctx['text']}" for ctx in retrieved_contexts]
    ) if retrieved_contexts else "No menu context available."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Restaurant menu context:\n{context_block}"},
    ]

    if conversation_history:
        for msg in conversation_history[-10:]:
            messages.append(msg)

    messages.append({"role": "user", "content": user_message})

    stream = await openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def check_allergy_safety(response_text: str, allergies: List[str]) -> Optional[str]:
    if not allergies:
        return None
    response_lower = response_text.lower()
    triggered = [a for a in allergies if a.lower() in response_lower]
    if triggered:
        warning = f"⚠️ Allergy Warning: The dish may contain {', '.join(triggered)}. Please check with staff before ordering."
        return warning
    return None
