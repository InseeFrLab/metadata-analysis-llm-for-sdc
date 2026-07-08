
from openai import OpenAI
import os

DEFAULT_BASE_URL = "https://llm.lab.sspcloud.fr/api/v1"  # INSEE SSP Cloud
DEFAULT_MODEL = "qwen3-6-35b-moe"
SENTINEL = "Aucune question."


def resolve_config(model=None, base_url=None):
    """Charge model / base_url / api_key depuis les variables d'environnement."""
    model = model or os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    base_url = base_url or os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("CLE_API_OPENWEBUI")
    if not api_key:
        raise RuntimeError(
            "Pas de clé API. Veuillez vérifier vos parametres de service sur Onyxia"
        )
    return {"model": model, "base_url": base_url, "api_key": api_key}


def chat(messages, *, model=None, base_url=None, temperature=0.0, max_tokens=65000):
    """LLM call"""
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


def is_auto_continued(reply: str) -> bool:
    """Vrai si le modele a repondu directement en JSON (pas de questions)."""
    parts = reply.split("\n---", 1)
    after = parts[1].strip() if len(parts) == 2 else reply.strip()
    return after.startswith(SENTINEL)
