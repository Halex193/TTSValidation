from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment


def text_to_speech(text, file_path):
    language = 'en'
    # file_object = gTTS(text=initial_text, lang=language, tld='ca', slow=False)
    file_object = gTTS(text=text, lang=language, slow=False)
    file_object.save(file_path)


def speech_to_text(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        recorded_audio = recognizer.record(source)
        text = recognizer.recognize_google(
            recorded_audio,
            language="en",
        )
        return text


def convert_mp3_to_wav(source, destination):
    # convert mp3 to wav
    sound = AudioSegment.from_mp3(source)
    sound.export(destination, format="wav")


def run_test(text, mp3_path, wav_path):
    text_to_speech(text, mp3_path)
    convert_mp3_to_wav(mp3_path, wav_path)
    return speech_to_text(wav_path)
