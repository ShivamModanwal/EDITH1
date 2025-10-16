from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os
import random
import pywhatkit
import time 
import pyautogui
import requests
import webbrowser
import tkinter as tk
import threading
import cv2
from PIL import Image, ImageTk

# Initialize Brave browser
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning Sir!")
    elif hour < 16:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("I am EDITH, your assistant. How can I assist you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return "None"
        except sr.RequestError:
            print("Network error.")
            return "None"

def openFolderOrFile():
    speak("Tell me the folder or file name.")
    query = takeCommand()
    base_dirs = ["C:\\", "D:\\", "E:\\"]  # Add directories to search
    for base in base_dirs:
        for root, dirs, files in os.walk(base):
            if query in dirs or query in files:
                os.startfile(os.path.join(root, query))
                speak(f"Opening {query}")
                return
    speak("Sorry, I couldn't find it.")

def performCalculation():
    speak("Tell me the calculation.")
    query = takeCommand()
    if query == "None":
        return
    query = query.replace("plus", "+").replace("minus", "-")
    query = query.replace("times", "*").replace("divided by", "/")
    try:
        result = eval(query)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def get_exchange_rate():
    speak("Tell me the source and target currency.")
    speak("Example: USD to INR")
    query = takeCommand()
    if "to" in query:
        source, target = query.split(" to ")
        url = f"https://api.exchangerate-api.com/v4/latest/{source.upper()}"
        try:
            response = requests.get(url).json()
            if target.upper() in response['rates']:
                rate = response['rates'][target.upper()]
                speak(f"1 {source.upper()} is {rate} {target.upper()}")
            else:
                speak("Invalid target currency.")
        except:
            speak("Unable to fetch exchange rates.")
    else:
        speak("Invalid format. Say: USD to INR.")

def edith_main():
    wishMe()
    while True:
        query = takeCommand()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak(results)
            except:
                speak("No results found.")
        elif 'open youtube' in query:
            speak("What do you want to watch?")
            pywhatkit.playonyt(takeCommand())
        elif 'open google' in query:
            speak("What should I search?")
            pywhatkit.search(takeCommand())
        elif 'open folder' in query or 'open file' in query:
            openFolderOrFile()
        elif 'calculate' in query:
            performCalculation()
        elif 'exchange' in query:
            get_exchange_rate()
        elif 'exit' in query:
            speak("Goodbye!")
            break

def start_gui():
    root = tk.Tk()
    root.title("EDITH Assistant")
    root.geometry("800x400")
    label = tk.Label(root, text="EDITH is ready.", font=("Arial", 16))
    label.pack(pady=20)
    def run_edith():
        threading.Thread(target=edith_main).start()
    button = tk.Button(root, text="Start", font=("Arial", 14), command=run_edith)
    button.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
