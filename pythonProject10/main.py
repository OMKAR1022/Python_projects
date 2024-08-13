import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print("You said:", text)

                # Check if the recognized command is "hello"
                if "hello" in text.lower():
                    print("Help")

            except sr.UnknownValueError:
                pass  # Ignore if speech is not recognized
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == "__main__":
    recognize_speech()