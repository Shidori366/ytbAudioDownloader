from pytube import YouTube
from unidecode import unidecode
import re

def printInfo(target: YouTube) -> YouTube.streams:
    print(target.author + " - " + target.title)

def download(url: str):
    targetToDownload = YouTube(url)
    print("Downloading audio from this target: ")
    printInfo(targetToDownload)
    audioStream = targetToDownload.streams.get_audio_only()
    temp = unidecode(targetToDownload.title.replace(" ", "_"))
    desiredFileName = ''.join(re.findall(r"[a-zA-Z0-9_]", temp))
    audioStream.download(filename=desiredFileName + ".mp3")

url = input("Enter url: ")
download(url)
