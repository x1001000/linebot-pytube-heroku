import os, sys, re
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from pytube import YouTube
from moviepy.editor import *

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# authenticate
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# callback HTTP POST call from LINE
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    for line in event.message.text.split():
        match = re.search('.*youtu.*', line)
        if match:
            print(YouTube(match.group(0)).streams.first().download(output_path='static',filename='YTDL'))
            video = VideoFileClip('static/YTDL.mp4')
            audio = video.audio
            audio.write_audiofile('static/LINE.mp3')
            video.close()
            audio.close()
            text='https://youtube-dl-linebot.herokuapp.com/static/LINE.mp3'
            #os.system('ffmpeg -i static/YTDL.mp4 -vn -c:a copy static/LINE.m4a')
            break
    else:    
        text = '說好的YouTube呢？'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')