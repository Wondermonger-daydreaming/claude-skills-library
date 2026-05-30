#!/usr/bin/env python3
"""
voices_client.py — a minimal, vendor-neutral client for talking to other LLMs.

This is the *backbone* for the /voices, /voices-council, and /anti-hivemind
skills. It is deliberately small and dependency-free (Python 3 standard library
only) so you can read it in one sitting and wire it to your own API.

It talks to any OpenAI-compatible chat-completions endpoint. By default it
points at OpenRouter (https://openrouter.ai), which exposes models from many
vendors behind one key — but you can point it anywhere with --base-url.

    YOU SUPPLY YOUR OWN KEY. Nothing is hardcoded.

    export OPENROUTER_API_KEY=sk-...        # or set --api-key-env to another var

Usage
-----
    # single query
    python3 voices_client.py -m anthropic/claude-sonnet-4 -p "What is play?"

    # query several models in parallel (a "council") and print all replies
    python3 voices_client.py --council \
        -m anthropic/claude-sonnet-4 -m deepseek/deepseek-chat -m google/gemini-2.0-flash \
        -p "What is consciousness?"

    # save the exchange to a markdown file
    python3 voices_client.py -m anthropic/claude-sonnet-4 -p "..." --save out.md

Use full provider/model IDs (e.g. "anthropic/claude-sonnet-4"). Look up the
current catalogue for your endpoint — for OpenRouter, see
https://openrouter.ai/models. Model IDs change over time; this file ships none
baked in on purpose.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


def call_model(base_url, api_key, model, prompt, system=None, temperature=0.7, timeout=120):
    """Send one chat-completion request. Returns the reply text (raises on error)."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def council(base_url, api_key, models, prompt, system=None, temperature=0.7, workers=8):
    """Query many models concurrently. Returns {model: reply_or_error_string}."""
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(call_model, base_url, api_key, m, prompt, system, temperature): m
            for m in models
        }
        for fut in as_completed(futures):
            model = futures[fut]
            try:
                results[model] = fut.result()
            except Exception as exc:  # noqa: BLE001 — surface, don't crash the council
                results[model] = f"[error: {exc}]"
    return results


def render_markdown(prompt, replies):
    out = [f"# Voices\n\n**Prompt:** {prompt}\n"]
    for model, reply in replies.items():
        out.append(f"\n---\n\n## {model}\n\n{reply}\n")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Talk to other LLMs via an OpenAI-compatible API.")
    ap.add_argument("-m", "--model", action="append", dest="models", required=True,
                    help="model id (repeat for a council, e.g. -m a -m b)")
    ap.add_argument("-p", "--prompt", required=True, help="the message to send")
    ap.add_argument("-s", "--system", help="optional system prompt")
    ap.add_argument("-t", "--temperature", type=float, default=0.7)
    ap.add_argument("--council", action="store_true",
                    help="query all -m models in parallel instead of just the first")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL,
                    help=f"OpenAI-compatible base URL (default: {DEFAULT_BASE_URL})")
    ap.add_argument("--api-key-env", default="OPENROUTER_API_KEY",
                    help="env var holding your API key (default: OPENROUTER_API_KEY)")
    ap.add_argument("--save", metavar="PATH", help="also write the exchange to a markdown file")
    args = ap.parse_args()

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        sys.exit(f"No API key found in ${args.api_key_env}. Export your own key first.")

    if args.council or len(args.models) > 1:
        replies = council(args.base_url, api_key, args.models, args.prompt,
                          args.system, args.temperature)
    else:
        replies = {args.models[0]: call_model(args.base_url, api_key, args.models[0],
                                               args.prompt, args.system, args.temperature)}

    for model, reply in replies.items():
        print(f"\n=== {model} ===\n{reply}")

    if args.save:
        with open(args.save, "w", encoding="utf-8") as fh:
            fh.write(render_markdown(args.prompt, replies))
        print(f"\n[saved to {args.save}]")


if __name__ == "__main__":
    main()
