import argparse
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator

parser = argparse.ArgumentParser(description="Speech to text")
parser.add_argument("file", help="The audio file to be processed")
translator = Translator()

recognizer = sr.Recognizer()

path_to_file = parser.parse_args().file
audio_file = AudioSegment.from_wav(path_to_file)
segment_length = 60000 # ms

start = 0
end = segment_length
i = 0
recognized_segments = []
with open("original.txt", "w") as original_file:
    with open("translated.txt", "w") as translated_file:

        while start < len(audio_file):
            segment = audio_file[start:end]
            segment.export(f"{path_to_file}_{i}.wav", format="wav")

            with sr.AudioFile(f"{path_to_file}_{i}.wav") as source:
                audio = recognizer.record(source)

                try:
                    text = recognizer.recognize_google_cloud(audio, language="hu-HU")
                    print("segment:", i)
                    # print(text)
                    # recognized_segments.append(text)
                    original_file.write(text + "\n")
                    translated_text = translator.translate(text, src="hu", dest="en").text
                    translated_file.write(translated_text + "\n")
                except sr.UnknownValueError:
                    print("Google Cloud Speech could not understand the audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Cloud Speech service; {e}")

            start += segment_length
            end += segment_length
            i += 1

