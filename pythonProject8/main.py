import pyttsx3

# Create TTS engine
engine = pyttsx3.init()

# Set welcome message
welcome_msg = "Welcome home!"

# Set TTS voice and speed
engine.setProperty('voice', 'english-us')
engine.setProperty('rate', 150)

# Say welcome message
engine.say(welcome_msg)
engine.runAndWait()
