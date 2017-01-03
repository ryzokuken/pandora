from os import system
import time

import speech_recognition
import pyttsx
from gtts import gTTS

def listen(recognizer, message='Say Something'):
    with speech_recognition.Microphone() as source:
        print(message)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except speech_recognition.UnknownValueError:
        try:
            return recognizer.recognize_sphinx(audio).lower()
        except speech_recognition.UnknownValueError:
            print("Pandora could not understand audio")
        except speech_recognition.RequestError as e:
            print("Sphinx error; {0}".format(e))
    except speech_recognition.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def speak(engine, message):
    try:
        tts = gTTS(text=message, lang='en')
        tts.save('out.mp3')
        system('mpg123 out.mp3 && rm out.mp3')
    except:
        engine.say(message)
        engine.runAndWait()

def initialize_engine():
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    return engine

def initialize_recognizer():
    recognizer = speech_recognition.Recognizer()
    return recognizer

def authenticate(engine, recognizer, user):
    speak(engine, 'Identify Yourself')
    if listen(recognizer) != user['name']:
        speak(engine, 'Unauthorized User')
        exit(1)
    speak(engine, 'What is your password, ' + user['name'] + '?')
    if listen(recognizer) != user['password']:
        speak(engine, 'Wrong Password')
        exit(1)
    speak(engine, 'Welcome, ' + user['name'])

def follow_command(engine, user, command):
    if 'goodbye' in command:
        speak(engine, 'Goodbye, ' + user['name'])
        exit(0)
    elif 'time' in command:
        speak(engine, 'The time is, ' + time.strftime('%I %M %p on %A, %B %e, %Y'))

def command_loop(engine, recognizer, user):
    while True:
        speak(engine, 'What is your command?')
        command = listen(recognizer)
        if 'pandora' in command:
            follow_command(engine, user, command)
        else:
            speak(engine, 'Was that meant for me?')
            if 'yes' in listen(recognizer):
                follow_command(engine, user, command)

def main():
    engine = initialize_engine()
    recognizer = initialize_recognizer()
    user = { 'name': 'god', 'password': 'hello world' }
    authenticate(engine, recognizer, user)
    command_loop(engine, recognizer, user)

if __name__ == '__main__':
    main()
