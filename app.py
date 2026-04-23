import os

import httpx
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_notification(name: str, phone: str, lang: str = "", level: str = "") -> None:
    lines = ["📬 Новая заявка с сайта!\n", f"👤 Имя: {name}", f"📞 Телефон: {phone}"]
    if lang:
        lines.append(f"🌍 Язык: {lang}")
    if level:
        lines.append(f"📊 Уровень: {level}")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    httpx.post(url, json={"chat_id": CHAT_ID, "text": "\n".join(lines)}, timeout=10)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name  = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    lang  = (data.get("lang") or "").strip()
    level = (data.get("level") or "").strip()

    if not name or not phone:
        return jsonify({"ok": False, "error": "Заполните все поля"}), 400

    send_telegram_notification(name, phone, lang, level)
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
