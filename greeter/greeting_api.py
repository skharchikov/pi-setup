from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/greeting')
def greeting():
    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "Generate a robot phrase that is said when human detector sensor detects a human. 60 tokens max, one sentence, extra short."}
                ]
            }
        )
        if res.status_code == 200:
            message = res.json()['choices'][0]['message']['content']
            return jsonify({"greeting": message})
        else:
            return jsonify({"greeting": "Hello there!"}), 200
    except Exception as e:
        return jsonify({"greeting": "Integration failed!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

