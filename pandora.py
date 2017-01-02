import sl4a
import time

def speak(droid, message):
    droid.ttsSpeak(message)
    while droid.ttsIsSpeaking()[1] == True:
        time.sleep(1)

def listen(droid, prompt='Speak Up'):
    return droid.recognizeSpeech(prompt).result.lower()

def auth(droid, user):
    speak(droid, 'Identify Yourself')
    if listen(droid) != user['name']:
        exit(1)
    speak(droid, 'What is your password, ' + user['name'])
    if listen(droid) != user['password']:
        exit(1)

def commandLoop(droid, user):
    while True:
        speak(droid, 'What is your command?')
        command = listen(droid)
        if 'goodbye' in command:
            speak(droid, 'Goodbye, ' + user['name'])
            exit(0)
        elif 'time' in command:
            speak(droid, time.strftime('%I %M %p on %A, %B %e, %Y'))

if __name__ == '__main__':
    droid = sl4a.Android()
    user = { 'name': 'god', 'password': 'hello world' }
    auth(droid, user)
    speak(droid, "Welcome, " + user['name'])
    commandLoop(droid, user)
