import os, json, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# === 1. Where to put your OpenRouter key ===
#   Copy the key from OpenRouter and paste it here.
OPENROUTER_KEY = "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"

#   Pick one model (a cheap, free‑tier one):
MODEL_ID = "openai/gpt-oss-20b:free"

@app.route("/llm", methods=["POST"])
def forward():
    # Retell sends a JSON block; we just forward it.
    data = request.get_json()

    # Build the payload for OpenRouter.
    payload = {
        "model": MODEL_ID,
        "messages": data.get("messages", [])
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_KEY}"
    }

    # Call OpenRouter.
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers
    )
    # If OpenRouter complains, we pass the message back to Retell.
    if resp.status_code != 200:
        return jsonify({"error": resp.text}), 502

    # Pull the answer text out of OpenRouter’s JSON.
    reply = resp.json()["choices"][0]["message"]["content"]

    # Return only what Retell wants:  {"answer": "..."}
    return jsonify({"answer": reply})

# Run the web‑server when we launch the script.
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000)
