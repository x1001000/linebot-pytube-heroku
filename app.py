import os, sys, re
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage, VideoSendMessage
from pytube import YouTube, extract
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
    for first in event.message.text.split():
        match = re.search('.*youtu.*', first)
        if match:
            url = match.group(0)
            video_id = extract.video_id(url)
            print(YouTube(url).streams.get_by_resolution('720p').download(output_path='static',filename=video_id))
            #video = VideoFileClip('static/YTDL.mp4')
            #audio = video.audio
            #audio.write_audiofile('static/LINE.mp3')
            #video.close()
            #audio.close()
            #text='https://youtube-dl-linebot.herokuapp.com/static/LINE.mp3'
            os.system(f'ffmpeg -i static/{video_id}.mp4 -vn -c:a copy static/{video_id}.m4a')
            try:
                line_bot_api.reply_message(
                    event.reply_token,[
                    VideoSendMessage(
                        original_content_url=f'https://youtube-dl-linebot.herokuapp.com/static/{video_id}.mp4',
                        preview_image_url=YouTube(url).thumbnail_url),
                    AudioSendMessage(
                        original_content_url=f'https://youtube-dl-linebot.herokuapp.com/static/{video_id}.m4a',
                        duration=YouTube(url).length * 1000),
                    TextSendMessage(text='還不手刀下載。。。')])
                break
            except:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='抱歉再試一次。。。'))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='說好的YouTube呢。。。'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')