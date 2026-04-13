import requests

BOT_TOKEN = "8766834595:AAH3vzgmj6MbRVzfBsKB6EYMeVjhP_veuU0"
CHAT_ID = "1081322945"


def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)