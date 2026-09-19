import os
import asyncio
from openai import AsyncOpenAI, RateLimitError, APIError, APIConnectionError, APITimeoutError
from fastapi import HTTPException
from pydantic import BaseModel

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_MODEL = os.getenv("FEATHERLESS_MODEL", "default-model-id")

client = AsyncOpenAI(
    api_key=FEATHERLESS_API_KEY,
    base_url="https://api.featherless.ai/v1",
    timeout=60.0,
    max_retries=0 # We handle retries manually to explicitly map errors
)

async def generate_response(messages: list, stream: bool = False, response_format=None):
    max_retries = 3
    base_delay = 1.0

    for attempt in range(max_retries + 1):
        try:
            kwargs = {
                "model": FEATHERLESS_MODEL,
                "messages": messages,
                "stream": stream,
            }
            if response_format:
                # For pydantic model, we can use the beta API if we want, or just json mode.
                # We will just pass the schema if they passed a pydantic model for structured outputs,
                # but to be safe with standard OpenAI SDK, we can use beta.chat.completions.parse
                pass
            
            if response_format and issubclass(response_format, BaseModel):
                return await client.beta.chat.completions.parse(
                    model=FEATHERLESS_MODEL,
                    messages=messages,
                    response_format=response_format
                )
            else:
                return await client.chat.completions.create(**kwargs)
        except RateLimitError:
            if attempt == max_retries:
                raise HTTPException(status_code=429, detail="Featherless rate limit exceeded")
            await asyncio.sleep(base_delay * (2 ** attempt))
        except APITimeoutError:
            if attempt == max_retries:
                raise HTTPException(status_code=504, detail="Upstream timeout")
            await asyncio.sleep(base_delay * (2 ** attempt))
        except APIConnectionError:
            if attempt == max_retries:
                raise HTTPException(status_code=502, detail="Upstream connection error")
            await asyncio.sleep(base_delay * (2 ** attempt))
        except APIError as e:
            status = getattr(e, 'status_code', 500)
            if status >= 500:
                if attempt == max_retries:
                    raise HTTPException(status_code=502, detail="Upstream failure")
                await asyncio.sleep(base_delay * (2 ** attempt))
            elif status == 429:
                if attempt == max_retries:
                    raise HTTPException(status_code=429, detail="Featherless rate limit exceeded")
                await asyncio.sleep(base_delay * (2 ** attempt))
            else:
                raise HTTPException(status_code=status, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
