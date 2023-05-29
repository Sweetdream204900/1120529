from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import requests

def checkword(w):
    url = 'https://www.moedict.tw/uni/' + w
    r = requests.get(url)
    datas = r.json()
    msg = '國字：' + datas['title'] + '\n'
    msg += '部首：' + datas['radical'] + '\n'
    msg += '筆劃：' + str(datas['stroke_count']) + '\n\n'
    for i in range(len(datas['heteronyms'])):
        msg += '注音：' + datas['heteronyms'][i]['bopomofo'] + '\n'
        msg += '拼音：' + datas['heteronyms'][i]['pinyin'] + '\n'    
        for j in range(len(datas['heteronyms'][i]['definitions'])):
            if 'type' in datas['heteronyms'][i]['definitions'][j]:
                msg += '[{}] {}\n'.format(
                    datas['heteronyms'][i]['definitions'][j]['type'],
                    datas['heteronyms'][i]['definitions'][j]['def'])
        msg += '\n'
    return msg

app = Flask(__name__)

line_bot_api = LineBotApi('l89AS7a8PRaA8g2PJEI5c0S9PUPNfl64P4BOFjv+Uobe8X9XlQBlsBGkHFi0gPFVWlM4Ce3QLo2dw8WZdDPOliQJMarGqrLIsIOgJbpQgjRxMXfHfv9T5kaUvoRbyPjUmbwYVVbc6PU1C83jXtdyKgdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('24a2517af359f276ec250dd5c5417d9f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=checkword(event.message.text)))


if __name__ == "__main__":
    app.run()
