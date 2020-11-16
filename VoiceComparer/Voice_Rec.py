import speech_recognition as sr
r = sr.Recognizer()
harvard = sr.AudioFile('harward.mp3')
with harvard as source :
    audio = r.rcord(source,duration=10)

type(audio)
r.recognize_google(audio)
