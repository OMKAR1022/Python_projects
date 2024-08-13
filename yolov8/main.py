import sounddevice as sd
import numpy as np
import speech_recognition as sr
from ultralytics import YOLO
import cv2
from gtts import gTTS
import os
import pygame
from pygame import mixer
import time
import depthai

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    mixer.init()
    mixer.music.load("output.mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove("output.mp3")

def recognize_speech():
    recognizer = sr.Recognizer()
    model = YOLO("yolov8n.pt")

    # Initialize DepthAI pipeline
    pipeline = depthai.Pipeline()

    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setPreviewSize(640, 480)
    cam_rgb.setInterleaved(False)
    cam_rgb.setFps(30)

    xout_rgb = pipeline.createXLinkOut()
    xout_rgb.setStreamName("rgb")
    cam_rgb.preview.link(xout_rgb.input)

    with depthai.Device(pipeline) as device, sr.Microphone() as source:
        print("Say 'hello' to start object detection:")
        recognizer.adjust_for_ambient_noise(source)

        q_rgb = device.getOutputQueue("rgb", maxSize=1, blocking=True)

        while True:
            print("Listening for the keyword...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print("You said:", text)

                if "hello" in text.lower():
                    speak("Hey! I am detecting objects. Please wait.")
                    detected_objects = set()

                    start_time = time.time()
                    detection_duration = 10  # Duration to perform continuous detection in seconds

                    while time.time() - start_time < detection_duration:
                        in_rgb = q_rgb.get()
                        frame = in_rgb.getCvFrame()

                        results = model.predict(source=frame, show=False)

                        for r in results:
                            boxes = r.boxes
                            for box in boxes:
                                c = box.cls
                                detected_objects.add(model.names[int(c)])

                    if detected_objects:
                        speak(f"Hey Omkar i detected the following objects : {', '.join(detected_objects)}")
                    else:
                        speak("No objects detected.")
                    break

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognize_speech()
