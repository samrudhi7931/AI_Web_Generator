from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import os
from dotenv import load_dotenv

load_dotenv()   # 1️⃣ Load .env file FIRST

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # 2️⃣ Read the key

print("API KEY LOADED:", bool(GROQ_API_KEY))  # 3️⃣ Debug (True/False only)




app = Flask(__name__)
generated_html = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    global generated_html

    prompt = request.json.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is empty"}), 400

    ai_prompt = f"""
    Generate a complete responsive HTML website with inline CSS.
    Include navbar, hero section, main content, and footer.
    Website description: {prompt}
    Return ONLY valid HTML.
    """

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",   # ✅ FIXED MODEL
            "messages": [{"role": "user", "content": ai_prompt}],
            "temperature": 0.4
        }
    )

    data = response.json()

    if response.status_code != 200:
        return jsonify({
            "error": "Groq API failed",
            "details": data
        }), 500

    generated_html = data["choices"][0]["message"]["content"]
    return jsonify({"html": generated_html})


@app.route("/download")
def download():
    global generated_html

    if not generated_html:
        return "No website generated yet", 400

    # Ensure folder exists
    os.makedirs("generated_sites", exist_ok=True)

    file_path = "generated_sites/index.html"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(generated_html)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
