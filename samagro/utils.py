import requests

KAVENEGAR_API_KEY = "SIZNING_KAVENEGAR_API_KALITINGIZ"

def send_sms(phone, code):
    # url = f"https://api.kavenegar.com/v1/{KAVENEGAR_API_KEY}/verify/lookup.json"
    # data = {"receptor": phone, "token": code, "template": "verify_code"}
    # response = requests.post(url, data=data)
    print(f"SMS yuborildi: {phone} - Tasdiqlash kodi: {code}")
    # return response.json()
    
