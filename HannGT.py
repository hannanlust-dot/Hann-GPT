import os
import time
import requests
import json

# === KONFIGURASI ===
TELEGRAM_TOKEN = os.getenv("8221579394:AAEi_FTuUSHcpgTWxAdZ2iKTrJg4mvAygCk") or "8221579394:AAEi_FTuUSHcpgTWxAdZ2iKTrJg4mvAygCk"
OPENROUTER_API_KEY = os.getenv("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") or "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"
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat"

# === FUNGSI AI ===
def ask_openrouter(prompt, system="Kamu adalah asisten AI Telegram Hannan. Jawab singkat, sopan, dan jelas."):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/hannan-openai",
        "X-Title": "Hannan Telegram AI"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Error:", e)
        return "⚠️ Maaf, AI lagi error atau koneksi lambat."


# === FUNGSI TELEGRAM ===
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 10, "offset": offset}
    resp = requests.get(url, params=params)
    return resp.json()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

# === LOOP UTAMA ===
def main():
    print("🤖 Bot Telegram AI aktif...")
    offset = None

    while True:
        try:
            updates = get_updates(offset)
            for result in updates.get("result", []):
                offset = result["update_id"] + 1
                message = result.get("message", {})
                text = message.get("text")
                chat_id = message.get("chat", {}).get("id")

                if not text:
                    continue

                print(f"Pesan dari Telegram: {text}")
                if text.lower() in ["/start", "hi", "halo"]:
                    send_message(chat_id, "Hai! Aku AI Telegram Hannan 🤖. Kirim pertanyaanmu!")
                    continue

                # panggil AI
                ai_reply = ask_openrouter(text)
                send_message(chat_id, ai_reply)

            time.sleep(1)
        except Exception as e:
            print("⚠️ Error loop:", e)
            time.sleep(3)


if __name__ == "__main__":
    main()
