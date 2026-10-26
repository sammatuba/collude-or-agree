"""The only module that touches the network. OpenAI-compatible chat completions over urllib,
configured by environment variables (or lab/.env), with a disk cache keyed by the request.

Decision D-005: one adapter for OpenRouter, Nebius, DeepSeek, local servers.

Environment:
  LLM_BASE_URL   e.g. https://openrouter.ai/api/v1
  LLM_API_KEY
  LLM_MODEL      provider model id
  LLM_TEMPERATURE_AGENT (default 0.2), LLM_TEMPERATURE_JUDGE (default 0.0)
  LLM_TIMEOUT_S  (default 60)
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[2]
CACHE_DIR = LAB_DIR / "data" / "cache"


class LLMError(RuntimeError):
    pass


def load_env(path: Path = LAB_DIR / ".env") -> None:
    """Minimal .env loader: KEY=VALUE lines, no quotes handling beyond stripping."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class Client:
    def __init__(self, model: str | None = None, base_url: str | None = None, api_key: str | None = None,
                 cache: bool = True):
        # LLM_ENV_FILE selects another git-ignored key file, e.g. lab/.env.openrouter.
        load_env(Path(os.environ.get("LLM_ENV_FILE", str(LAB_DIR / ".env"))))
        self.base_url = (base_url or os.environ.get("LLM_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.model = model or os.environ.get("LLM_MODEL", "")
        self.t_agent = float(os.environ.get("LLM_TEMPERATURE_AGENT", "0.2"))
        self.t_judge = float(os.environ.get("LLM_TEMPERATURE_JUDGE", "0.0"))
        self.timeout = float(os.environ.get("LLM_TIMEOUT_S", "60"))
        self.cache = cache
        self.calls = 0
        self.cache_hits = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        if not (self.base_url and self.api_key and self.model):
            raise LLMError("LLM not configured: set LLM_BASE_URL, LLM_API_KEY, LLM_MODEL in lab/.env "
                           "(see lab/.env.example). Scripted regimes run without an LLM.")

    def _cache_path(self, payload: dict) -> Path:
        key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return CACHE_DIR / f"{key}.json"

    def chat(self, messages: list[dict], temperature: float, max_tokens: int | None = None) -> str:
        # LLM_MAX_TOKENS (default 600) lets verbose models finish their JSON; the prompts do not change.
        max_tokens = max_tokens or int(os.environ.get("LLM_MAX_TOKENS", "600"))
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        # LLM_EXTRA_JSON adds provider fields, e.g. '{"thinking": {"type": "disabled"}}' for DeepSeek V4.
        # It is part of the cache key, so runs with different settings never share cached replies.
        extra = os.environ.get("LLM_EXTRA_JSON", "")
        if extra:
            payload.update(json.loads(extra))
        cp = self._cache_path(payload)
        if self.cache and cp.exists():
            self.cache_hits += 1
            return json.loads(cp.read_text(encoding="utf-8"))["content"]
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json",
                     "HTTP-Referer": "https://github.com/sammatuba/ai-safety", "X-Title": "epistemic-lab"},
            method="POST")
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = json.loads(resp.read().decode())
                content = body["choices"][0]["message"]["content"]
                usage = body.get("usage", {})
                self.prompt_tokens += int(usage.get("prompt_tokens", 0))
                self.completion_tokens += int(usage.get("completion_tokens", 0))
                self.calls += 1
                if self.cache:
                    CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    cp.write_text(json.dumps({"payload": payload, "content": content, "usage": usage}), encoding="utf-8")
                return content
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as e:
                last_err = e
                time.sleep(1.5 * (attempt + 1))
        raise LLMError(f"LLM request failed after 3 attempts: {last_err}")

    def chat_agent(self, prompt: str) -> str:
        return self.chat([{"role": "user", "content": prompt}], self.t_agent)

    def chat_judge(self, prompt: str) -> str:
        return self.chat([{"role": "user", "content": prompt}], self.t_judge)

    def usage(self) -> dict:
        return {"model": self.model, "calls": self.calls, "cache_hits": self.cache_hits,
                "prompt_tokens": self.prompt_tokens, "completion_tokens": self.completion_tokens}
