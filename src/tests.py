import os

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
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

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
        error_sum=0

        for line in data_file:
            mp3_path = f"{mp3_folder}/test{i}.mp3"
            wav_path = f"{wav_folder}/test{i}.wav"
            try:
                result = run_test(line.rstrip(), mp3_path, wav_path)
            except Exception as e:
                print("SKIP...")
            if not keep_audio:
                os.remove(mp3_path)
                os.remove(wav_path)
            print(f"Initial Text {i}: {line}")
            print(f"Decoded Text {i}: {result}")

            error = wer(line.split(), result.split())

            error = 1-((len(line)-error)/len(line))

            error_sum+=error
            print(f"Error {i}: {error}")

            i += 1

        total_error = error_sum/(i-1)
        print(f"Average error: {total_error}")
