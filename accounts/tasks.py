from celery import shared_task
from user.settings import API_KEY
from celery import Celery
import requests
import redis

redis_code = redis.Redis(host='redis', port=6380, db=0, charset='utf-8', decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379')


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
        "x-api-key": API_KEY
    }
    requests.post(url, json=data, headers=headers)
