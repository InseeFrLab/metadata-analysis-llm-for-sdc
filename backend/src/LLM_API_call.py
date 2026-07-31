
import os
import re

from openai import OpenAI

DEFAULT_BASE_URL = "https://llm.lab.sspcloud.fr/api/v1"  # INSEE SSP Cloud
DEFAULT_MODEL = "qwen3-6-35b-moe"
SENTINEL = "Aucune question."
FORCE_JSON_INSTRUCTION = (
    "Vous avez deja recu une reponse du producteur a vos questions. Aucun "
    "autre tour de questions n'est possible. Ne posez plus de questions. "
    "Produisez maintenant le tableau JSON final selon le contrat de sortie de "
    "la Phase 2 : pour toute ambiguite restante, faites le meilleur choix "
    "possible et consignez-la dans la note d'incertitude residuelle apres le "
    "\"]\"."
)

# Un rappel generique ("produisez le JSON") ne dit pas au modele *ce qui* cloche :
# un tableau bien forme mais de mauvaise forme (croisements aplatis en
# spanning_1 / hrc_spanning_1 au lieu de spanning_variables) traverse une telle
# relance inchange. On lui rend donc les erreurs du validateur.
_ERR_LOC = re.compile(r"^\s*at [^:]*:\s*")
_MAX_DISTINCT_ERRORS = 8


def schema_repair_instruction(errors: list[str]) -> str:
    """Relance corrective apres un echec de validation du schema.

    Les erreurs se repetent a l'identique sur chaque enregistrement (26 lignes
    fautives = 26 fois le meme couple de messages) : on les deduplique en
    retirant leur position, pour que la relance porte le defaut plutot que son
    volume."""
    seen = []
    for err in errors:
        msg = _ERR_LOC.sub("", err).strip()
        if msg and msg not in seen:
            seen.append(msg)
    shown = seen[:_MAX_DISTINCT_ERRORS]
    reste = len(seen) - len(shown)
    if reste > 0:
        shown.append(f"(et {reste} autre(s) type(s) d'erreur)")

    return (
        "Le tableau JSON que vous venez d'emettre a ete rejete par la validation "
        "du schema :\n"
        + "\n".join(f"- {m}" for m in shown)
        + "\n\nReemettez le tableau complet en respectant exactement le contrat "
        "de sortie du §1 : les six cles, sans en ajouter, renommer ni supprimer "
        "aucune. Les variables de croisement vont dans la cle imbriquee "
        "\"spanning_variables\": [{\"code\": \"...\", \"hrc\": \"...\"}] — jamais "
        "en colonnes aplaties spanning_1 / hrc_spanning_1, que le programme "
        "derive lui-meme en aval. Ne changez pas le contenu des lignes, "
        "uniquement leur structure si elle est en cause."
    )


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


def chat(messages, *, model=None, base_url=None, temperature=0.0, max_tokens=None):
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
