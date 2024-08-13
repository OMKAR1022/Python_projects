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

    # Create RGB Camera node
    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setBoardSocket(depthai.CameraBoardSocket.RGB)  # Correct usage for RGB
    cam_rgb.setPreviewSize(640, 480)
    cam_rgb.setInterleaved(False)
    cam_rgb.setFps(30)

    # Create Stereo Depth node
    stereo = pipeline.createStereoDepth()
    stereo.setLeftRightCheck(True)
    stereo.setExtendedDisparity(True)
    stereo.setSubpixel(True)
    stereo.setDepthAlign(depthai.CameraBoardSocket.RGB)  # Align depth with RGB

    # Create left and right camera nodes
    cam_left = pipeline.createMonoCamera()
    cam_left.setBoardSocket(depthai.CameraBoardSocket.LEFT)  # Use LEFT for left camera
    cam_left.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_720_P)

    cam_right = pipeline.createMonoCamera()
    cam_right.setBoardSocket(depthai.CameraBoardSocket.RIGHT)  # Use RIGHT for right camera
    cam_right.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_720_P)

    # Link cameras to stereo depth node
    cam_left.out.link(stereo.left)
    cam_right.out.link(stereo.right)

    # Create output streams for RGB and Depth
    xout_rgb = pipeline.createXLinkOut()
    xout_rgb.setStreamName("rgb")
    cam_rgb.preview.link(xout_rgb.input)

    xout_depth = pipeline.createXLinkOut()
    xout_depth.setStreamName("depth")
    stereo.depth.link(xout_depth.input)

    with depthai.Device(pipeline) as device, sr.Microphone() as source:
        print("Say 'hello' to start object detection:")
        recognizer.adjust_for_ambient_noise(source)

        q_rgb = device.getOutputQueue("rgb", maxSize=1, blocking=True)
        q_depth = device.getOutputQueue("depth", maxSize=1, blocking=True)

        while True:
            print("Listening for the keyword...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print("You said:", text)

                if "hello" in text.lower():
                    speak("Hey! I am detecting objects. Please wait.")
                    detected_objects = {}  # Dictionary to store objects with their distances

                    start_time = time.time()
                    detection_duration = 10  # Duration to perform continuous detection in seconds

                    while time.time() - start_time < detection_duration:
                        in_rgb = q_rgb.get()
                        in_depth = q_depth.get()

                        frame = in_rgb.getCvFrame()
                        depth_frame = in_depth.getFrame()

                        # Process depth frame to get distance information
                        depth_data = np.array(depth_frame, dtype=np.float32)
                        depth_data_cm = depth_data / 10.0  # Convert from millimeters to centimeters

                        # Compute the average distance of valid pixels
                        valid_depths = depth_data_cm[depth_data_cm > 0]
                        if valid_depths.size > 0:
                            avg_distance = np.mean(valid_depths)

                            results = model.predict(source=frame, show=False)
                            for r in results:
                                boxes = r.boxes
                                for box in boxes:
                                    c = box.cls
                                    obj_name = model.names[int(c)]

                                    # Add object with distance to the dictionary
                                    if obj_name not in detected_objects:
                                        detected_objects[obj_name] = avg_distance/2

                    if detected_objects:
                        obj_distances = ', '.join([f"{obj} at {dist:.2f} cm" for obj, dist in detected_objects.items()])
                        speak(f"Hey Omkar, I detected the following objects: {obj_distances}")
                    else:
                        speak("No objects detected.")
                    break

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == "__main__":
    recognize_speech()