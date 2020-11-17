from flask import Flask, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route("/")
def hello():
    print(YouTube('https://youtu.be/T1dcfK10K8g').streams.first().download(filename='static/ytdl'))
    return 'static/ytdl.mp4'