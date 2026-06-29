#!/usr/bin/env python3
from openai import OpenAI
import os

DEFAULT_BASE_URL = "https://llm.lab.sspcloud.fr/api/v1"  # INSEE SSP Cloud
DEFAULT_MODEL = "qwen3-6-35b-moe"


def _load_dotenv():
    """Best-effort: load a gitignored .env so keys can stay out of the shell history."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


def resolve_config(model=None, base_url=None):
    """Resolve model / base_url / api_key from args then env. Raises if no key."""
    _load_dotenv()
    model = model or os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    base_url = base_url or os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("CLE_API_OPENWEBUI")
    if not api_key:
        raise RuntimeError(
            "No API key found. Set OPENAI_API_KEY or CLE_API_OPENWEBUI in your .env."
        )
    return {"model": model, "base_url": base_url, "api_key": api_key}


def chat(messages, *, model=None, base_url=None, temperature=0.0, max_tokens=100000):
    """Send a full `messages` list to the model and return the assistant text.

    `messages` is the OpenAI chat shape, e.g.
        [{"role": "system", "content": <prompt>},
         {"role": "user", "content": <metadata>}, ...]
    Temperature defaults to 0 for the most deterministic output the model allows.
    """
    cfg = resolve_config(model, base_url)
    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
    resp = client.chat.completions.create(
        model=cfg["model"],
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}}
    )
    choice = resp.choices[0]
    content = choice.message.content

    # A reply cut off at the token cap is incomplete — its JSON array would fail
    # validation downstream with a confusing parse error. Fail loud and point at the cause.
    if getattr(choice, "finish_reason", None) == "length":
        raise RuntimeError(
            f"Model output was truncated at the token cap (max_tokens={max_tokens}, "
            "finish_reason='length'). The reply is incomplete; raise max_tokens and retry."
        )

    if content is None:
        raise RuntimeError(
            "Model returned empty content (message.content is None). "
            "This usually means the model is in extended-thinking mode and the reply "
            "is in a different field. Check the model's thinking settings or add "
            "/no_think to the system prompt."
        )
    return content
