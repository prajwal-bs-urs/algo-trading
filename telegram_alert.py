import os
import requests


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def _credentials_available() -> bool:
    """Return True only when both environment variables are set."""
    if not BOT_TOKEN or not CHAT_ID:
        print("Warning: BOT_TOKEN or CHAT_ID not set. Telegram alert skipped.")
        return False
    return True


def send_message(message: str) -> None:
    if not _credentials_available():
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    response = requests.post(url, data=payload, timeout=10)
    if not response.ok:
        print(f"Telegram sendMessage failed: {response.status_code} {response.text}")


def send_photo(photo_path: str) -> None:
    if not _credentials_available():
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:
        response = requests.post(
            url,
            files={"photo": photo},
            data={"chat_id": CHAT_ID},
            timeout=30,
        )

    if not response.ok:
        print(f"Telegram sendPhoto failed: {response.status_code} {response.text}")
