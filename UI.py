import speech_recognition as sr
import pyttsx3
from roastedbyai import Conversation, Style
import streamlit as st
import time

# Streamlit settings
st.set_page_config(page_title="Roasting AI Chatbot", page_icon="🔥")

# Store user information
user_data = {}


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.markdown("""
            <div style="text-align:center;">
                <div class="listening-animation" style="width: 100px; height: 100px; background-color: lightcoral; border-radius: 50%; animation: pulse 1s infinite;"></div>
            </div>
            <style>
                @keyframes pulse {
                    0% { transform: scale(0.95); }
                    70% { transform: scale(1.1); }
                    100% { transform: scale(0.95); }
                }
            </style>
            """, unsafe_allow_html=True)

            st.write("🎙️ Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
    except AssertionError:
        st.error("Microphone is not accessible. Please ensure it's properly connected and enabled.")
        return None

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Couldn't understand you. Please try again.")
        return None
    except sr.RequestError:
        st.error("Error with the speech recognition service.")
        return None


def generate_prompt(user_input):
    # Generate a roasting prompt using stored user data
    return f"The user is named {user_data['name']}, likes {user_data['hobby']}, has a pet {user_data['pet']}, loves {user_data['favorite_food']}, and struggles with {user_data['worst_habit']}. They just said: '{user_input}'. Roast them mercilessly!"


def main():
    st.title("🔥 Roasting AI Chatbot")
    st.write("Hey there! Before we start roasting, I need to know a few things about you.")

    if "conversation" not in st.session_state:
        st.session_state.conversation = Conversation(Style.valley_girl)

    user_data['name'] = st.text_input("What's your name?")
    user_data['hobby'] = st.text_input("What's something you like to do?")
    user_data['pet'] = st.text_input("Do you have a pet? If so, what kind?")
    user_data['favorite_food'] = st.text_input("What's your favorite food?")
    user_data['worst_habit'] = st.text_input("What's a habit of yours you secretly wish you could quit?")

    if st.button("Start Chatting"):
        speak(f"Alright {user_data['name']}, I'm ready for your weak attempts at roasting me! Let's see what you got!")

        while True:
            user_input = listen()
            if user_input:
                prompt = generate_prompt(user_input)
                response = st.session_state.conversation.send(prompt)

                st.markdown("""
                <div style="text-align:center;">
                    <div class="speaking-animation" style="width: 100px; height: 100px; background-color: lightblue; border-radius: 50%; animation: bounce 1s infinite;"></div>
                </div>
                <style>
                    @keyframes bounce {
                        0% { transform: translateY(0); }
                        50% { transform: translateY(-10px); }
                        100% { transform: translateY(0); }
                    }
                </style>
                """, unsafe_allow_html=True)

                st.write(f"AI: {response}")
                speak(response)

            if user_input and ("bye" in user_input.lower() or "exit" in user_input.lower()):
                break

        st.session_state.conversation.kill()
        st.write("Goodbye!")


if __name__ == "__main__":
    main()
