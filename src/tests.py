import os
from math import sqrt

from main_functions import *
import pyttsx3


def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    # initialisation
    import numpy
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]


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
        accuracy_sum = 0

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

            error = wer(line.split(), result.split())

            local_accuracy = (len(line) - error) / len(line)

            accuracy_list.append(local_accuracy)

            accuracy_sum += local_accuracy
            if verbose:
                print(f"Initial Text {i}: {line}")
                print(f"Decoded Text {i}: {result}")
            print(f"Accuracy {i}: {local_accuracy * 100:.3f}%")

            i += 1

        total_accuracy = accuracy_sum / (i - 1)

        std_dev = 0
        for accuracy in accuracy_list:
            std_dev += (accuracy - total_accuracy) ** 2

        std_dev /= len(accuracy_list)
        std_dev = sqrt(std_dev)
        return total_accuracy, std_dev


def main():
    create_folder(files_folder)
    create_folder(mp3_folder)
    create_folder(wav_folder)

    files = ['medicine_data', 'culinary_data', 'artistic_data', 'lyrics_data']

    results = []

    for file in files:
        file_path = f'{files_folder}/{file}.txt'
        total_accuracy, std_dev = test_file(file_path)
        print(f"Average accuracy for {file_path}: {total_accuracy * 100:.3f}, Standard deviation {std_dev * 100:.3f}")
        results.append((file_path, total_accuracy, std_dev))

    print("\nFinal results:")
    for result in results:
        print(f"Average accuracy for {result[0]}: {result[1] * 100:.3f}, Standard deviation {result[2] * 100:.3f}")


if __name__ == "__main__":
    keep_audio = False
    verbose = False
    files_folder = 'files'
    mp3_folder = f'{files_folder}/mp3-files'
    wav_folder = f'{files_folder}/wav-files'
    main()
