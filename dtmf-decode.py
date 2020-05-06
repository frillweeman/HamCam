from subprocess import Popen, PIPE, STDOUT, DEVNULL
from threading import Thread
import re

process = Popen(
    "multimon-ng -a DTMF", stdout=PIPE, stderr=STDOUT, shell=True)


def speak(text):
    Popen(f'sleep 1 && espeak "{text}"',
          stdout=DEVNULL, stderr=STDOUT, shell=True)


def sendImage():
    Thread(target=speak, args=(
        "sending image Sending image in Robot 24. Please wait.",)).start()
    Popen("raspistill -vf -hf -w 320 -h 240 -o /home/pi/out.jpg && python3 -m pysstv --vox /home/pi/out.jpg /home/pi/output.wav --mode Robot24BW --chan 1 && espeak \"sending image\" && mplayer /home/pi/output.wav",
          stdout=DEVNULL, stderr=STDOUT, shell=True)


shellDTMFPattern = re.compile(r"DTMF:\s(.)")

while True:
    line = process.stdout.readline().decode("utf-8")
    if not line:
        break

    match = shellDTMFPattern.search(line)
    if match:
        dtmf = match.group(1)
        if dtmf == '9':
            # request photo
            print("writing image")
            sendImage()
            # txImg = mode(Image.open("/home/pi/test.jpg"), 48000, 16)
            # txImg.write_wav("test.wav")
        else:
            speak(
                f"you pressed You pressed {dtmf}. That's an invalid choice. Press 9 for an image.")
