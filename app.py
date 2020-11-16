from flask import Flask
from pytube import YouTube

app = Flask(__name__)

@app.route("/")
def hello():
    YouTube('https://youtu.be/T1dcfK10K8g').streams.first().download(filename='ytdl')
    return "Hello World!"