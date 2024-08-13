import os

import cv2
import numpy as np
import mysql.connector

def match_images(image_database, image_camera):
  """Matches an image in the camera with an image in the database.

  Args:
    image_database: A list of images in the database.
    image_camera: The image captured by the camera.

  Returns:
    The index of the image in the database that matches the image in the camera.
  """

  # Connect to the MySQL database.
  connection = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Mysql@123",
      database="Omk")

  # Fetch the images from the database.
  cursor = connection.cursor()
  cursor.execute("SELECT image FROM pic")
  images_database = []
  for row in cursor:
    images_database.append(row[0])

  # Extract features from the images.
  features_database = []
  for image in images_database:
    image = cv2.imdecode(np.fromstring(image, np.uint8), cv2.IMREAD_COLOR)
    kp, des = cv2.xfeatures2d.SURF_create(400).detectAndCompute(image, None)
    features_database.append(des)

  features_camera = cv2.xfeatures2d.SURF_create(400).detectAndCompute(image_camera, None)

  # Match the features from the camera image with the features in the database.
  index_params = dict(algorithm=cv2.FLANN_INDEX_KDTREE, trees=5)
  matcher = cv2.FlannBasedMatcher(index_params, {})
  matches = matcher.knnMatch(features_camera, features_database, k=2)

  # Find the best match.
  best_match = None
  best_score = 0
  for match1, match2 in matches:
    score = match1.distance / match2.distance
    if score > best_score:
      best_match = match1
      best_score = score

  # Return the index of the best match.
  if best_match is None:
    return -1
  else:
    return best_match.queryIdx

if _name_ == "_main_":
  # Load the images in the database.
  image_database = []
  for filename in os.listdir("images"):
    image_database.append(cv2.imread("images/" + filename))

  # Capture an image from the camera.
  image_camera = cv2.VideoCapture(0).read()[1]

  # Match the image in the camera with the images in the database.
  index = match_images(image_database, image_camera)

  # Print the index of the matched image.
  print(index)