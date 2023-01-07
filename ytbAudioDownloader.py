from pytube import YouTube
from unidecode import unidecode
import re

fileSize = 0

def printProgress(stream, chunk, bytes_remaining):
    progress = 100 - ((bytes_remaining * 100) / fileSize)
    formattedRemaining = "{:.2f}".format(progress) + '%'
    print("Progress: " + formattedRemaining, end='\r')

def completeMessage(stream, file_path):
    print("Successfully downloaded at: ", file_path)

def download(url: str):
    global fileSize
    targetToDownload = YouTube(url, on_progress_callback=printProgress, on_complete_callback=completeMessage)
    print("Downloading audio from this target: ")
    print(targetToDownload.title)
    audioStream = targetToDownload.streams.get_audio_only()
    fileSize = audioStream.filesize
    temp = unidecode(targetToDownload.title.replace(" ", "_"))
    desiredFileName = ''.join(re.findall(r"[a-zA-Z0-9_]", temp))
    audioStream.download(filename=desiredFileName + ".mp3")

while True: 
    url = input("Enter url: ")
    try: 
        download(url)
    except:
        print("Couldn't download from this source")
