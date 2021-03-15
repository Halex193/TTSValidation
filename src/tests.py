import os
from math import sqrt
import fastwer
import re

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


def test_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Please create the file {file_path} with texts on separate lines")
    print(f"Testing {file_path}")
    accuracy_list = []

    with open(file_path) as data_file:
        i = 1
        accuracy_sum = (0, 0)

        for line in data_file:
            mp3_path = f"{mp3_folder}/test{i}.mp3"
            wav_path = f"{wav_folder}/test{i}.wav"
            try:
                result = run_test(line.rstrip(), mp3_path, wav_path)
            except FileNotFoundError:
                result = ''
            except AssertionError:
                result = ''

            if not keep_audio:
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                if os.path.exists(wav_path):
                    os.remove(wav_path)

            word_count1 = len(re.findall(r'\w+', line))
            length1 = len(line)
            length2 = len(result)
            if word_count1 == 0 or length2 == 0:
                error = (100, 100)
            else:
                error = (fastwer.score([line], [result]) / word_count1, fastwer.score([line], [result], True) / length1)

            local_accuracy = (100 - error[0], 100-error[1])

            accuracy_list.append(local_accuracy)

            accuracy_sum = (accuracy_sum[0] + local_accuracy[0], accuracy_sum[1] + local_accuracy[1])
            if verbose:
                print(f"Initial Text {i}: {line}")
                print(f"Decoded Text {i}: {result}")
            print(f"Accuracy {i}: WER - {local_accuracy[0]:.3f}%, CER - {local_accuracy[1]:.3f}%")

            i += 1

        final_accuracy = (accuracy_sum[0] / (i - 1), accuracy_sum[1] / (i - 1))

        std_dev = (0, 0)
        for accuracy in accuracy_list:
            std_dev = (std_dev[0] + (accuracy[0] - final_accuracy[0]) ** 2, std_dev[1] + (accuracy[1] - final_accuracy[1]) ** 2)

        std_dev = (sqrt(std_dev[0] / len(accuracy_list)), sqrt(std_dev[1] / len(accuracy_list)))
        return final_accuracy, std_dev


def main():
    create_folder(files_folder)
    create_folder(mp3_folder)
    create_folder(wav_folder)

    files = ['medicine_data', 'culinary_data', 'artistic_data', 'lyrics_data']

    results = []

    for file in files:
        file_path = f'{files_folder}/{file}.txt'
        total_accuracy, std_dev = test_file(file_path)
        print(f"Dataset {file_path}:")
        print(f"WER - Accuracy: {total_accuracy[0]:.3f}%, Standard deviation: {std_dev[0]:.3f}%")
        print(f"CER - Accuracy: {total_accuracy[1]:.3f}%, Standard deviation: {std_dev[1]:.3f}%")
        print()
        results.append((file_path, total_accuracy, std_dev))

    print("\nFinal results:")
    for result in results:
        print(f"Dataset {result[0]}:")
        print(f"WER - Accuracy: {result[1][0]:.3f}%, Standard deviation: {result[2][0]:.3f}%")
        print(f"CER - Accuracy: {result[1][1]:.3f}%, Standard deviation: {result[2][1]:.3f}%")
        print()


if __name__ == "__main__":
    keep_audio = False
    verbose = False
    files_folder = 'files'
    mp3_folder = f'{files_folder}/mp3-files'
    wav_folder = f'{files_folder}/wav-files'
    main()
