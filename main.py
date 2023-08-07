import speech_recognition as sr
import pyttsx3
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import en_core_web_sm
import sys
from playsound import playsound
import time
from hugchat import hugchat
from hugchat.login import Login


sign = Login('ooo99900036@gmail.com', '%ifz;;yAc7efR*m')
cookies = sign.login()
sign.saveCookiesToDir()
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())


nlp = en_core_web_sm.load()

# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
client_id = "2e8ddac3a5bf4b3ca2d0ee6108cdf616"
client_secret = "a99777a279504b74a3b5f03aa1d770f1"
redirect_uri = "https://localhost:3033"  # Replace with your desired redirect URI
scope = "user-modify-playback-state"  # Specify the required scope for controlling playback
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))


def listen():
    with sr.Microphone() as source:

        print("Listening...")
        playsound("C:/Users/D4RK_D4NTE/PycharmProjects/pythonProject2/venv/Open.mp3")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

        # Set a timeout and a silence threshold
        r.pause_threshold = 0.8  # Maximum pause between words (in seconds)
        r.phrase_threshold = 0.6  # Minimum length of a phrase (in seconds)
        audio = r.listen(source, timeout=10)  # Apply noise reduction
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
        doc = nlp(query)
        return doc
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
    return None


def play_track(track_name):
    results = sp.search(q=track_name, type="track", limit=1)
    if len(results["tracks"]["items"]) > 0:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
        print(f"Now playing: {track_name}")
    else:
        print("Sorry, the track could not be found.")


def listen_yes_no():
    with sr.Microphone() as source:
        print("Listening for yes or no...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        response = r.recognize_google(audio)
        print("You said:", response)
        return response.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
    return ""


# Function to speak the response
def speak(response):
    sentences = response.split(".")  # Split the response into sentences
    stop_count = 0  # Counter for the number of encountered full stops
    for sentence in sentences:
        sentence = sentence.strip()
        engine.say(sentence)
        engine.runAndWait()
        stop_count += 1
        if stop_count == 1:
            break


# Function to process user commands
def process_command(command):
    command_str = str(command)
    doc = nlp(command_str)
    intent = doc[0].text  # Get the first token as the intent
      # Convert the doc to string
    if 'play' in intent:
        playsound("C:/Users/D4RK_D4NTE/PycharmProjects/pythonProject2/venv/Succeed.mp3")
        track_name = extract_track_name(command_str)
        if track_name:
            play_track(track_name)
        else:
            speak("I'm sorry, I didn't understand the track name.")
    elif 'stop' in intent:
        playsound("C:/Users/D4RK_D4NTE/PycharmProjects/pythonProject2/venv/Succeed.mp3")
        sp.pause_playback()
        print("Music playback stopped.")
    elif 'open' in intent:
        playsound("C:/Users/D4RK_D4NTE/PycharmProjects/pythonProject2/venv/Succeed.mp3")
        website = extract_website(command)
        if website:
            speak(f"Opening {website}...")
            webbrowser.open(f"https://www.{website}.com")
        else:
            speak("I'm sorry, I didn't understand which website to open.")
    elif 'bye' in intent:
        playsound("C:/Users/D4RK_D4NTE/PycharmProjects/pythonProject2/venv/Succeed.mp3")
        speak("Goodbye! Have a great day!")
        sys.exit()  # Use sys.exit() to exit the program
    else:
        query_1 = (str(command))
        response = chatbot.chat(query_1)
        if 'assist with something else' in response.lower() or 'how can i assist you' in response.lower():
            speak(response)
            # Listen for the query after the chatbot's response
            query = listen()
            while query is None:
                speak("Sorry, I didn't catch that. Could you please repeat?")
                query = listen()
            process_command(query)
        else:
            speak(response)


# Function to extract website from user command
def extract_website(command):
    keywords = ["open", "visit", "go to"]
    for keyword in keywords:
        website = command.text.replace(keyword, "").strip()
        return website
    return None


# Function to extract question from user command
def extract_question(command):
    # Remove the keyword "search" from the command
    question = command.text.replace("search", "").strip()
    return question


def extract_track_name(command):
    # Remove the "play" keyword from the command
    command = command.replace("play", "").strip()
    # Extract the track name using pattern matching
    pattern = r"([\w\s]+)"  # Matches alphanumeric characters and spaces
    match = re.search(pattern, command)
    if match:
        return match.group(1)  # Return the extracted track name
    else:
        return None  # Return None if no match found


# Function to handle the wake word detection
def handle_wake_word():
    while True:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

            timeout_duration = 5  # Set the timeout duration (in seconds)
            start_time = time.time()  # Get the start time
            detected = False  # Flag to indicate if wake word is detected

            while time.time() - start_time < timeout_duration:
                audio = r.listen(source, phrase_time_limit=5)  # Apply noise reduction

                try:
                    print("Recognizing wake word...")
                    query = r.recognize_google(audio, language='en-in')
                    print("You said:", query)
                    doc = nlp(query)
                    v = list(doc)  # Convert doc to a list
                    if any(token.text.lower() == "crypt" or "crept" for token in v):
                        print("Wake word detected!")
                        detected = True
                        break  # Exit the loop if wake word is detected
                except sr.UnknownValueError:
                    print("Sorry, I didn't catch that. Could you please repeat?")
                except sr.RequestError:
                    print("Sorry, there was an issue with the speech recognition service.")

            if detected:
                return True

            print("Wake word not recognized. Listening again...")


# Main loop for interaction
while True:
    handle_wake_word()
    query = listen()
    while query is None:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        query = listen()
    process_command(query)
