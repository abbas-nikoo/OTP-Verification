from celery import shared_task
from user.settings import API_KEY
from celery import Celery
import requests
import redis

redis_code = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379')
# API_KEY = "k0CjatRjRGtvxgPjO2EhgSEwINn92CtpFhRUn9DjAQlbPRrjjjpCLUZ4YG8ythRq"


# @app.task()
@shared_task()
def send_sms(phone, random_code):
    redis_code.set(phone, random_code, ex=100)

    url = 'https://api.sms.ir/v1/send/verify/'
    data = {
        "mobile": phone,
        "templateId": 100000,
        "parameters": [
            {
                "name": "Code",
                "value": random_code
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "x-api-key": 'mExkaRq3ufX0QRbcJHF8TJK6eaCbIDVu0qINuof311C7dcrdgIfexxyetIBppngb'
    }
    requests.post(url, json=data, headers=headers)
