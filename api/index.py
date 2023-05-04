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

app = Flask(__name__)

line_bot_api = LineBotApi('EK1/2bq1epRMJuSC7LFfkouKJPJgtLW1X310gSQbRTHvnCmFiMJy+bZG7bPCGMQgWYDxjlMJy/WAtE99i6Y+pCp3kCFYW92pH/3akVF/GdWLGY4DSDqIQHySFHMYnH5iuQ7yzCrX6HYdiMYsu1OPlwdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('7c715fb8323313d689440b50218dcd9b')

@app.route("/")
def home():
    return "LINE BOT API Server is running"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()