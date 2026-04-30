"""Thin Gemini Flash wrapper for the AI Astrologer chat.

Uses Google's REST API directly (no SDK dependency, keeps the API surface tiny).
Reads the key from GEMINI_API_KEY env var. If the key is missing, returns a
safe stub message so dev/test still works.
"""
from __future__ import annotations

import json
import os
from typing import Optional

import requests


GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL_TMPL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)


class GeminiUnavailable(RuntimeError):
    """Raised when GEMINI_API_KEY is not set or the API call fails."""


def ask_gemini(
    *,
    system_prompt: str,
    user_message: str,
    history: Optional[list[dict]] = None,
    timeout_s: float = 30.0,
    temperature: float = 0.7,
    max_output_tokens: int = 800,
) -> str:
    """Call Gemini Flash with the system prompt + chart context, plus the native's question.

    Args:
        system_prompt: From `make_system_prompt(context, locale)`.
        user_message: The native's question.
        history: Optional prior turns [{role: 'user'|'model', text: '...'}].

    Returns:
        The model's text response.

    Raises:
        GeminiUnavailable: if no API key or HTTP error.
    """
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise GeminiUnavailable("GEMINI_API_KEY not set")

    contents: list[dict] = []
    for turn in history or []:
        role = "model" if turn.get("role") == "model" else "user"
        contents.append({"role": role, "parts": [{"text": turn.get("text", "")}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        },
    }

    url = GEMINI_URL_TMPL.format(model=GEMINI_MODEL, key=key)
    try:
        r = requests.post(url, json=payload, timeout=timeout_s)
    except requests.RequestException as e:
        raise GeminiUnavailable(f"network error: {e}") from e

    if r.status_code != 200:
        raise GeminiUnavailable(f"HTTP {r.status_code}: {r.text[:300]}")

    try:
        data = r.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise GeminiUnavailable(f"no candidates: {json.dumps(data)[:300]}")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        if not text:
            raise GeminiUnavailable("empty response")
        return text
    except (KeyError, ValueError) as e:
        raise GeminiUnavailable(f"parse error: {e}") from e
