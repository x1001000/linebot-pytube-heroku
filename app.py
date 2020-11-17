from flask import Flask
from pytube import YouTube
from moviepy.editor import *

app = Flask(__name__)

@app.route("/")
def hello():
    print(YouTube('https://youtu.be/T1dcfK10K8g').streams.first().download(output_path='static',filename='ytdl'))
    video = VideoFileClip('static/ytdl.mp4')
    audio = video.audio
    audio.write_audiofile('static/line.mp3')
    video.close()
    audio.close()
    return 'OK'