import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

AIkey = os.getenv("OPEN_AI")
NewsKey = os.getenv("newskey")

def ai(c):
    client = OpenAI(api_key=f"{AIkey}"
)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": f"{c} and rememer you are an virtual assistan named jarvis and try to keep the response as short as possible"}
    ]
    )

    return (completion.choices[0].message.content)

def processCommand(c):
    print(c)
    if(c.lower() == "open youtube"):
        webbrowser.open("https://www.youtube.com")
    # elif(c.lower() == "what is gassy" or "what is gassy?"):
    #     speak("Gassy is a padodi who release gas through her stomach at very small intervals of time and it is very smelly gas brotha eww")
    elif("open google" in c.lower()):
        webbrowser.open("https://www.google.com")
    elif(c.lower().startswith("play")):
        song = c.lower().split(" ",1)[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif("news" in c.lower()):
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&apiKey={NewsKey}")
        if r.status_code == 200:
            data=r.json()
            articles = data.get('articles', [])
            
            if not articles:
                speak("No news articles found.")
            else:
                for article in articles[:5]:  # Limit to 5 articles to avoid too much output
                    speak(article['title'])
        else:
            speak("Failed to fetch the news. Please try again later.")
    else:
        #let ai handle
        Aioutput = ai(c)
        speak(Aioutput) 
    
    print(c)

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()
    
if __name__ == "__main__":
    speak("Initiliazing jarvis...")
    while True:
        r = sr.Recognizer()
       
        
        
        print("recognizing.....")
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya?")
                with sr.Microphone() as source:
                    print("jarvis active.....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(command)
                    processCommand(command)
                        
        except Exception as e:
            print("Aapne  to meri boolti hee baand kardee")