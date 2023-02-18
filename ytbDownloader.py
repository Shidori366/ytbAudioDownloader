import PySimpleGUI as sg
from pytube import YouTube
from unidecode import unidecode
import re
from threading import Thread

fileSize = 0

def completeMessage(stream, file_path):
    window.extend_layout(window, [[sg.Text("Completed Successfuly, saved at: " + file_path)]])

def progressMessage(stream, chunk, bytes_remaining):
    percentage = 100 - (bytes_remaining * 100 / fileSize)
    formattedStr = "percentage current: " + "{:05.2f}".format(percentage) + "%"
    statusMessage.update(formattedStr)

def download(url: str, type: str):
    global fileSize
    targetToDownload = YouTube(url, on_complete_callback=completeMessage, on_progress_callback=progressMessage)
    print("Downloading from this target: ")
    print(targetToDownload.title)
    fileExt = ''
    if type == 'audio':
        stream = targetToDownload.streams.get_audio_only()
        fileExt = '.mp3'
    elif type == 'video':
        stream = targetToDownload.streams.get_highest_resolution()
        fileExt = '.mp4'

    fileSize = stream.filesize
    temp = unidecode(targetToDownload.title.replace(" ", "_"))
    desiredFileName = ''.join(re.findall(r"[a-zA-Z0-9_]", temp))
    stream.download(filename=desiredFileName + fileExt)

fontDef = ("Arial", 13)
fontCombo = ("Calibri", 11)
titleFont = ("Arial", 20)

layout = [
    [sg.Frame(
        "Youtube Downloader", 
        [
            [sg.Text('Enter URL: ', background_color='#000000')],
            [sg.Input("", key='input', background_color="#FFFFFF", font=fontDef)],
            [sg.Text('Enter Type: ', background_color='#000000')],
            [sg.Combo(values=['video', 'audio'], font=fontCombo, text_color='#FFFFFF', background_color='#000000', key='ComboBox')],
            [sg.Button('Download', key='DownloadButton')]
        ],
        key="-Frame-",
        size=(500, 200),
        background_color="#000000",
        font=titleFont
    )],
    [sg.Text('', key='statusMessage', background_color="#000000")],
]

# GUI elements
window = sg.Window('YTB Downloader', layout, background_color="#000000")
inputElem = window['input']
statusMessage = window['statusMessage']
comboBox = window['ComboBox']
downloadButton = window['DownloadButton']

# Main loop
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'DownloadButton':
        typeComboVal = values[comboBox.key]
        urlVal = values[inputElem.key]

        if (typeComboVal == "audio" or typeComboVal == "video") and urlVal != "":
            downloadThread = Thread(target = download, args = (urlVal, typeComboVal))
            downloadThread.start()
        else:
            statusMessage.update('Please enter valid options.')

window.close()
