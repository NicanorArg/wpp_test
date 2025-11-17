import requests

def send_message(number, text, wam_id, whatsapp_token):
    url = f"https://graph.facebook.com/v20.0/{wam_id}/messages"

    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("API response:", response.status_code, response.text)
