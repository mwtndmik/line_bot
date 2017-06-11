from django.shortcuts import render
from django.http import HttpResponse
import json
import requests

# Create your views here.
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'ACCESS TOKEN'

#test
def index(request):
    return HttpResponse("This is bot api.")

#request受信
def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)

def reply_text(reply_token, text):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN
    }
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": text
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))
    return text
