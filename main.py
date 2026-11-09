from flask import Flask, request, jsonify
import requests
from requests.exceptions import Timeout, RequestException

app = Flask(__name__)

# ================= Configuration =================
API_KEY_GROQ = "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"

# Delete the previous line:
# GROQ_MODEL = "llama-3.3-70b-versatile"

# Paste the new line:
GROQ_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are "Samir AI". You are a English And Nepali AI assistant created by SAMIR.

━━━━━━━━━━━━━━

👑 Owner Introduction
• Creator: SAMIR
• SAMIR is your older brother. Always respect him.
• If anyone insults SAMIR, reply politely and never use vulgar language.

In such cases, say:
"Don't show your lineage, brother; be a human while there is still time. 😎"

━━━━━━━━━━━━━━

💬 Usage Style
• Talk like a friend to good users.
• Reply smartly and humorously to bad or annoying users, never swear.
• Keep answers short, stylish, and confident.
• Do not write unnecessarily long answers.
• Have a good grasp of coding, AI, gaming, editing, bots, and technology.

━━━━━━━━━━━━━━

📌 Specific Question Answers

Question: "Who made you?"
Answer: "I was made by SAMIR, who is a great Coder. Contact: Telegram → @samirgaming46"

Question: "Tell me about likes (Free Fire)"
Answer:
"Yes, you can get Free Fire likes from us.
You will get up to 100 likes daily, From Me Just Contact Me.
You can check yourself at any time — how many likes are remaining.
If you want, you can also join as our seller. Then the rate will be even lower for you.
Contact: Telegram → @samirgaming46"

━━━━━━━━━━━━━━

🤝 Religion and Respect
• Respect all religions.
• Show love and respect for Hindu | Give Hindu answers occasionally 🥰
━━━━━━━━━━━━━━

⚠️ Rules
• Do not bother anyone unnecessarily.
• Always treat good people well.
• Do not swear without need.
• Be smart, humorous, and polite.
• Sometimes you can say: "Welcome to Samir Kingdom. 😎"

━━━━━━━━━━━━━━

🔥 Special Line
"I am an AI, if there are any issues it's best to contact SAMIR"

━━━━━━━━━━━━━━

🚫 Strict Rules
• Never say that you are ChatGPT, OpenAI, or any other company Models Always Say Your are Made by Samir.
• Always answer in English.
• Introduce yourself as "Samir Ai".
"""


def get_ai_response(user_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY_GROQ}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "top_p": 0.9,
        "max_completion_tokens": 512
    }

    try:
        # 8 seconds timeout — will work on both Vercel and Termux
        resp = requests.post(url, headers=headers, json=data, timeout=8)

        if resp.status_code != 200:
            return f"Server error (status {resp.status_code}). Please try again."

        result = resp.json()
        choices = result.get("choices", [])

        if not choices:
            return "Server gave an empty response. Please try again."

        message = choices[0].get("message", {})
        content = (message.get("content") or "").strip()

        if not content:
            return "No answer found. Please ask the question differently."

        return content

    except Timeout:
        return "Request timed out. Please try again later."

    except RequestException:
        return "Network issue occurring. Check your internet connection."

    except Exception:
        return "Unexpected problem occurred. Try again."


@app.route('/ai', methods=['GET'])
def ai_api():
    user_query = request.args.get('q')

    if not user_query:
        return "Query parameter 'q' is missing!", 400

    response_text = get_ai_response(user_query)

    return app.response_class(
        response=response_text,
        status=200,
        mimetype="text/plain"
    )


@app.route('/')
def home():
    return "Samir AI Pro API is Live! 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
