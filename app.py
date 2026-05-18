import json
import os
import time
from collections import defaultdict
from html import escape
from typing import Dict, List
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".")

QUOTES_FILE = "quotes.json"
MAX_QUOTE = 500
MAX_NAME = 60
MAX_CONTEXT = 120
RATE_WINDOW = 300   # seconds
RATE_MAX = 3        # submissions per IP per window

_rate_store: Dict[str, List[float]] = defaultdict(list)


def load_quotes() -> list:
    if not os.path.exists(QUOTES_FILE):
        return []
    with open(QUOTES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_quotes(quotes: list) -> None:
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)


def _pin() -> str:
    pin = os.environ.get("GUESTBOOK_PIN", "")
    if not pin:
        raise RuntimeError("GUESTBOOK_PIN environment variable is not set")
    return pin


def _allowed(ip: str) -> bool:
    now = time.time()
    _rate_store[ip] = [t for t in _rate_store[ip] if now - t < RATE_WINDOW]
    if len(_rate_store[ip]) >= RATE_MAX:
        return False
    _rate_store[ip].append(now)
    return True


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/quotes", methods=["GET"])
def get_quotes():
    return jsonify(load_quotes())


@app.route("/api/quotes", methods=["POST"])
def add_quote():
    ip = request.remote_addr

    if not _allowed(ip):
        return jsonify({"error": "Too many submissions — slow down."}), 429

    data = request.get_json(silent=True) or {}

    if data.get("pin", "") != _pin():
        return jsonify({"error": "Wrong PIN."}), 403

    quote = escape(str(data.get("quote", "")).strip())[:MAX_QUOTE]
    name = escape(str(data.get("name", "Anonymous")).strip())[:MAX_NAME] or "Anonymous"
    context = escape(str(data.get("context", "")).strip())[:MAX_CONTEXT]

    if not quote:
        return jsonify({"error": "Quote cannot be empty."}), 400

    entry = {
        "id": int(time.time() * 1000),
        "quote": quote,
        "name": name,
        "context": context,
        "date": time.strftime("%Y-%m-%d"),
    }

    quotes = load_quotes()
    quotes.append(entry)
    save_quotes(quotes)

    return jsonify(entry), 201


if __name__ == "__main__":
    try:
        _pin()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        print("Set it with: export GUESTBOOK_PIN=yourpin")
        raise SystemExit(1)

    app.run(host="0.0.0.0", port=5000, debug=False)
