import pyttsx3
from flask import Flask
import datetime
import json

import speech_recognition as sr

app = Flask(__name__)

name_List = ["john", "alex", "aryan", "peter", "tom"]
member_Id = ["1234", "1424", "4623", "7375", "8270"]

class _Voice:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty("rate",160)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

        #self.engine.setProperty('voice', voices[1].id)

    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()
questions = [
    'Please say yes if you can count on your family/Caregiver for help and support? otherwise say No ',
    '''What would you like the practitioner to focus on in your visit? Here are your options 
    1) Lifestyle changes to improve my health
    2) Preventive screenings or vaccinations
    3) Resources to help in my daily life
    4) Medications
    5) Managing chronic conditions
    6) Public health concerns
    7) No issues or Not applicable
     ''',

    'Please say Yes if you had 3 or more emergency room visits in the last three months otherwise say No',
    'Please say Yes if you are using an assistive device otherwise say No',
    'Please say Yes if you receiving any outside services otherwise say No'
]
answers = []




def speak(audio):
    tts = _Voice()
    tts.start(audio)
    del(tts)
    

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am calling from the HouseCalls program to verify your appointment tomorrow.")

    speak("May I ask you some questions in preparation for your HouseCalls visit. ")	
    user_ans = takeCommand().lower()
    if(user_ans == 'yes'):
        speak("Please verify your name.")
        name = takeCommand().lower()
    else:
        speak("Sure, we will remind you later.")
        exit(0)
    return name
countSpeak = 0

def takeCommand():
    global countSpeak
    secondAns = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 1
        audio = r.listen(source)
        
        
    try:
        print("Recognizing..")
        query= r.recognize_google(audio, language="en-in")
        print("User said:", query)

    except Exception as e:
        print(e)
        if(countSpeak<1):
            print("Say that again please....")
            speak("Say that again please.")
            countSpeak = countSpeak + 1
            secondAns = takeCommand().lower()
            if(secondAns != "None"):
                countSpeak = 0
                return secondAns


        countSpeak = 0
        return "None"
        
    return query
@app.route("/index", methods=["GET"])
def alexa():
    name = wishMe()
    counter = 0
    #counter = len(questions)
    if(name.lower() in name_List):
        name_Index = name_List.index(name.lower())
        print("Thank You for confirming your name.")
        speak("Thank You for confirming your name.")
        speak("Please verify your insurance number.")

        mid = takeCommand().lower()
        if(member_Id[name_Index] == mid):
            print("Thank You for confirming your insurance number.")
            speak("Thank You for confirming your insurance number.")
            while(counter<len(questions)):
                speak(questions[counter])
                print(f"Question no {counter + 1} : {questions[counter]}")
                query = takeCommand().lower()
                #query = "Delhi"
                answers.append(query)
                counter = counter + 1
            print("Thank you for participating in the HouseCalls Program.  Looking forward to see you tomorrow.")
            speak("Thank you for participating in the HouseCalls Program.  Looking forward to see you tomorrow.")
            questions.append("Name")
            answers.append(name)
            questions.append("mid")
            answers.append(mid)

        else:
            mid = ""
            print("Sorry, your insurance number is incorrect.. ")
            speak("Sorry, your insurance number is incorrect.. ")
    else:
        name = ""
        print("Sorry, your name does not exist in our system.. ")
        speak("Sorry, your name does not exist in our system.. ")
        

    #print(questions)
    #print(answers)

    dictionary = dict(zip(questions, answers))
    print(dictionary)

    with open('data.json', 'w') as f:
        json.dump(dictionary, f)
    #takeCommand()

    
    return dictionary
if __name__ =="__main__":
    app.debug = False
    app.run('127.0.0.1', port=5000)