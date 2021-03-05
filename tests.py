import os

from main_functions import *
import pyttsx3

def speech_test(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def speech_to_text_live_data():
    r = sr.Recognizer()

    while 1:
        try:
            with sr.Microphone() as source2:
                print("Adjusting noise ")
                r.adjust_for_ambient_noise(source2, duration=1)
                print("Recording for 4 seconds")
                audio2 = r.listen(source2, timeout=4)
                print("Done recording")
                myText = r.recognize_google(audio2)
                myText = myText.lower()

                print(myText)
                speech_test(myText)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


if __name__ == "__main__":
    keep_audio = True
    files_folder = 'files'
    mp3_folder = f'{files_folder}/mp3-files'
    wav_folder = f'{files_folder}/wav-files'
    data_file_path = f'{files_folder}/data.txt'

    create_folder(files_folder)
    create_folder(mp3_folder)
    create_folder(wav_folder)

    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"Please create the file {data_file_path} with texts on separate lines")

    with open(data_file_path) as data_file:
        i = 1
        for line in data_file:
            mp3_path = f"{mp3_folder}/test{i}.mp3"
            wav_path = f"{wav_folder}/test{i}.wav"
            result = run_test(line.rstrip(), mp3_path, wav_path)
            if not keep_audio:
                os.remove(mp3_path)
                os.remove(wav_path)
            print(f"Decoded Text {i}: {result}")
            i += 1

