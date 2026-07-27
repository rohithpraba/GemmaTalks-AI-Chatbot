"""GemmaTalks: a local Ollama-backed chat prototype with streamed responses."""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterator
from typing import Any

import gradio as gr
import requests

LOGGER = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3")
CONNECT_TIMEOUT_SECONDS = float(os.getenv("CONNECT_TIMEOUT_SECONDS", "5"))
READ_TIMEOUT_SECONDS = float(os.getenv("READ_TIMEOUT_SECONDS", "180"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
GRADIO_HOST = os.getenv("GRADIO_HOST", "127.0.0.1")
GRADIO_PORT = int(os.getenv("GRADIO_PORT", "7860"))


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "".join(parts)
    return str(content)


def build_ollama_messages(message: str, history: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Convert Gradio's OpenAI-style history to Ollama chat messages."""
    ollama_messages: list[dict[str, str]] = []
    for item in history:
        role = item.get("role")
        if role not in {"system", "user", "assistant"}:
            continue
        ollama_messages.append(
            {"role": role, "content": _content_to_text(item.get("content", ""))}
        )
    ollama_messages.append({"role": "user", "content": message})
    return ollama_messages


def stream_ollama_response(
    message: str, history: list[dict[str, Any]]
) -> Iterator[str]:
    """Yield the accumulated Ollama response for Gradio streaming."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": build_ollama_messages(message, history),
        "stream": True,
    }

    try:
        with requests.post(
            OLLAMA_CHAT_URL,
            json=payload,
            stream=True,
            timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
        ) as response:
            response.raise_for_status()
            accumulated = ""
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    LOGGER.warning("Ignoring a non-JSON Ollama stream line")
                    continue

                chunk = event.get("message", {}).get("content", "")
                if chunk:
                    accumulated += chunk
                    yield accumulated

            if not accumulated:
                yield "The model returned no text."
    except requests.RequestException:
        LOGGER.exception("Ollama request failed")
        yield (
            "Unable to reach the local Ollama service. Confirm that Ollama is "
            f"running and that model '{OLLAMA_MODEL}' is available."
        )


def build_demo() -> gr.ChatInterface:
    return gr.ChatInterface(
        fn=stream_ollama_response,
        title="GemmaTalks",
        description=(
            "Local Ollama-backed chat prototype. Public sharing is disabled by "
            "default and must be explicitly enabled."
        ),
        flagging_mode="never",
        api_visibility="private",
    )


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    build_demo().launch(
        server_name=GRADIO_HOST,
        server_port=GRADIO_PORT,
        share=GRADIO_SHARE,
        pwa=True,
    )
