import pyttsx3
from decouple import config
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib

if '__main__' == __name__:

    USERNAME = config('USER')
    BOTNAME = config('BOTNAME')

    engine = pyttsx3.init('sapi5')

    # Set Rate
    engine.setProperty('rate', 190)

    # Set Volume
    engine.setProperty('volume', 1.0)

    # Set Voice (Female)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)


def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()

    from datetime import datetime

    def greet_user():
        """Greets the user according to the time"""

        hour = datetime.now().hour
        if (hour >= 6) and (hour < 12):
            speak(f"Bonjour {USERNAME}")
        elif (hour >= 12) and (hour < 16):
            speak(f"Bonjour {USERNAME}")
        elif (hour >= 16) and (hour < 19):
            speak(f"Bonsoir {USERNAME}")
        speak(f"Je suis {BOTNAME}. Comment puis-je vous aidez ?")

        import speech_recognition as sr
        from random import choice
        from utils import opening_text

        def take_user_input():
            """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

            r = sr.Recognizer()
            with sr.Microphone() as source:
                print('Listening....')
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                print('Recognizing...')
                query = r.recognize_google(audio, language='fr-fr')
                if not 'exit' in query or 'stop' in query:
                    speak(choice(opening_text))
                else:
                    hour = datetime.now().hour
                    if hour >= 21 and hour < 6:
                        speak("Bonne nuit monsieur, faites de beaux rêves")
                    else:
                        speak('Passez une bonne journée monsieur')
                    exit()
            except Exception:
                speak('Désolé, je n/ai pas compris. pouvez vous répétez ?')
                query = 'None'
            return query

        """def open_camera():
            sp.run('start microsoft.windows.camera:', shell=True)

            def open_discord():
                os.startfile(paths['discord'])

                def open_cmd():
                    os.system('start cmd')

                    def search_on_wikipedia(query):
                        results = wikipedia.summary(query, sentences=2)
                        return results"""
