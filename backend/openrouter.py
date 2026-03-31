"""OpenRouter API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, OPENROUTER_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via OpenRouter API.

    Args:
        model: OpenRouter model identifier (e.g., "openai/gpt-4o")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 8000,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                print(f"Error querying model {model}: HTTP {response.status_code}")
                print(f"Response body: {response.text[:500]}")
                return None

            data = response.json()

            if 'error' in data:
                print(f"API error for model {model}: {data['error']}")
                return None

            message = data['choices'][0]['message']
            # Ensure we always have some content to return
            content = message.get('content')
            if not content:
                # If the model returned tool calls without direct content, serialize them
                if 'tool_calls' in message:
                    content = f"[Tool calls: {message['tool_calls']}]"
                else:
                    content = "[No content returned]"
            return {
                'content': content,
                'reasoning_details': message.get('reasoning_details')
            }

    except httpx.TimeoutException:
        print(f"Timeout querying model {model} (timeout={timeout}s)")
        return None
    except Exception as e:
        print(f"Error querying model {model}: {type(e).__name__}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of OpenRouter model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
