import pyttsx3
import requests
import wikipedia
import pywhatkit as kit
from flask import Flask
from email.message import EmailMessage
import smtplib
from decouple import config
import speech_recognition
from random import choice
from utils import opening_text
from datetime import datetime

USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init()

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    print(hour)
    if (hour >= 6) and (hour < 12):
        speak(f"Bonjour {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Bonjour {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Bonsoir {USERNAME}")
    speak(f"Je suis  {BOTNAME}. Comment puis-je vous aidez ?")


def take_user_input():
        """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print('Listening....')
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='fr-fr')
            if not 'exit' in query or 'stop' in query or 'cancel' in query:
                speak(choice(opening_text))
            else:
                hour = datetime.now().hour
                if hour >= 21 and hour < 6:
                    speak("Bonne nuit")
                else:
                    speak('Bonne journée')
                exit()
        except Exception:
            speak('Pouvez-vous répéter s il vous plait ?')
            query = 'None'
            take_user_input()
        return query


def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    greet_user()
    #engine.say("I am happy")
    for index, name in enumerate(speech_recognition.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    while True:
        query = take_user_input().lower()

        if 'ouvre notepad' in query:
            open_notepad()

        elif 'ouvre discord' in query:
            open_discord()

        elif 'ouvre invité de commande' in query or 'open cmd' in query:
            open_cmd()

        elif 'allume la camera' in query:
            open_camera()

        elif 'ouvre la calculatrice' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('Que cherchez-vous sur Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"Selon Wikipedia, {results}")
            speak("Je vous l'affiche sur votre écran sir.")
            print(results)

        elif 'youtube' in query:
            speak('Que voulez vous lancer sur Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'recherche sur google' in query:
            speak('Que cherchez-vous sur Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "envoie un message whatsapp " in query:
            speak('Sur quel numéro voulez vous envoyer un message ? entrez le numéro dans la commande: ')
            number = input("Enter the number: ")
            speak("Quel est le message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("Message envoyé sir.")

        elif "envoie un email" in query:
            speak("A quelle adresse mail voulez vous envoyer un message sir? Entrez l'adresse dans la commande: ")
            receiver_address = input("Enter email address: ")
            speak("Quel est l'objet sir?")
            subject = take_user_input().capitalize()
            speak("Quel est le message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("Mail envoyé sir.")
            else:
                speak("Quelque chose s'est mal passer pendant l envoie du mail.")

        elif 'raconte une blague' in query:
            speak(f"Voici une blague : ")
            joke = get_random_joke()
            speak(joke)

        elif "avis" in query:
            speak(f"voici un avis pour vous, sir")
            advice = get_random_advice()
            speak(advice)

        elif "Films " in query:
            speak(f"Voici les derniers films tendances : {get_trending_movies()}")
            speak("je vous les affichent sur votre écran sir.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"Voici la dernière actualité, sir")
            speak(get_latest_news())
            speak("je vous les affichent sur votre écran sir.")
            print(*get_latest_news(), sep='\n')

        elif 'Quel temps il fait' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://www.lachainemeteo.com/{ip_address}/city/").text
            speak(f"Voici la méteo de {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"La température actuelle est de {temperature}")
            speak(f"Le bulletin méteo dit : {weather}")
            speak("Je vous l'affiche sur votre écran.")
            print(f"Description: {weather}\nTemperature: {temperature}\n")
