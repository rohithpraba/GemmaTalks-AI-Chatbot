import json
from unittest.mock import patch

import requests

import app as gemmatalks


class FakeResponse:
    def __init__(self, lines, status_code=200):
        self.lines = lines
        self.status_code = status_code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def iter_lines(self, decode_unicode=True):
        del decode_unicode
        yield from self.lines


def test_build_messages_preserves_history_and_adds_current_message():
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]
    assert gemmatalks.build_ollama_messages("Next", history) == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "user", "content": "Next"},
    ]


def test_stream_accumulates_chunks():
    lines = [
        json.dumps({"message": {"content": "Hel"}}),
        json.dumps({"message": {"content": "lo"}}),
    ]
    with patch.object(gemmatalks.requests, "post", return_value=FakeResponse(lines)):
        output = list(gemmatalks.stream_ollama_response("Hi", []))
    assert output == ["Hel", "Hello"]


def test_stream_ignores_invalid_json_line():
    lines = ["not-json", json.dumps({"message": {"content": "OK"}})]
    with patch.object(gemmatalks.requests, "post", return_value=FakeResponse(lines)):
        output = list(gemmatalks.stream_ollama_response("Hi", []))
    assert output == ["OK"]


def test_network_error_returns_controlled_message():
    with patch.object(
        gemmatalks.requests, "post", side_effect=requests.ConnectionError("secret detail")
    ):
        output = list(gemmatalks.stream_ollama_response("Hi", []))
    assert len(output) == 1
    assert "Unable to reach the local Ollama service" in output[0]
    assert "secret detail" not in output[0]
