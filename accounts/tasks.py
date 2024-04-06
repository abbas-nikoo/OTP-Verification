from celery import shared_task
from user.settings import API_KEY
from celery import Celery
import requests
import redis

redis_code = redis.Redis(host='redis', port=6379, db=0, charset='utf-8', decode_responses=True)
app = Celery('tasks', backend='redis://redis', broker='redis://redis:6379/0')


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
        "x-api-key": 'k0CjatRjRGtvxgPjO2EhgSEwINn92CtpFhRUn9DjAQlbPRrjjjpCLUZ4YG8ythRq'
    }
    requests.post(url, json=data, headers=headers)



#
# import requests
# from celery import Celery
#
# app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:63/0')
#
# API_KEY = API_KEY
# SMS_ENDPOINT = "https://api.sms.ir/v1/send/verify"
#
#
# @app.task()
# def send_sms(phone, random_code):
#     data = {
#         "mobile": phone,
#         "templateId": 100000,
#         "parameters": [
#             {
#                 "name": "Code",
#                 "value": random_code
#             }
#         ]
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "text/plain",
#         "x-api-key": API_KEY
#     }
#     response = requests.post(SMS_ENDPOINT, json=data, headers=headers)
#     print(response.json())
