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

import markov_bot

# import sentencepiece as spm

# from SentensePiece import reply


app = Flask(__name__)

app.config['CHANNEL_ACCESS_TOKEN'] = 'BBRbzcN0GjBelHIlfA0QkwsCGqN5kNVJcH9m5kEO//OPT74Ml0i5YAjHeEWUHU1HmAUfsJ/7bn6mQ1v1yQQSTIkZBnCdDDTrCrpqV3jORXuEy2oiPUXsLSbgjd6LHz1kdFnvcJxIWbpj0qrrlXewiwdB04t89/1O/w1cDnyilFU='
app.config['CHANNEL_SECRET'] = '21a4d78b5cd16fe7b22580095a364185'

line_bot_api = LineBotApi(app.config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['CHANNEL_SECRET'])

friend = markov_bot.LineFriend("ファイル名")


@app.route("/")
def say_hello():
    return "Hello"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # sp = spm.SentencePieceProcessor()

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sentence = friend.make_sentence(
        reply_to=event.message.text,
        replier=friend.name,
    )

    text = sentence.replace('[Begin]', '')

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text),
    )


if __name__ == "__main__":
    app.run()
