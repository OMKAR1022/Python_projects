import os
import pickle
import face_recognition
import cv2
import firebase_admin

from firebase_admin import db
from firebase_admin import credentials, storage

cred = credentials.Certificate("/Users/omkar/Downloads/credentials.json")
firebase_admin.initialize_app(cred, options={
    'storageBucket': "smart-goggle-9e64d.appspot.com"
})

bucket = storage.bucket()

#local_image_path = '/Users/omkar/Downloads/goggle.png'

#firebase_storage_path = 'images/image.jpg'

##blob.upload_from_filename(local_image_path)

#print(f'Image uploaded to Firebase Storage at: {blob.public_url}')

#firebase_storage_path = 'images/image.jpg'  # Adjust the path as needed
#blob = bucket.blob(firebase_storage_path)

# Download the image to a local file
#local_download_path = 'Images/'  # Specify the local download path
#blob.download_to_filename(local_download_path)

#print(f'Image downloaded to: {local_download_path}')

firebase_storage_path = 'images'

# Local directory in the project to save downloaded images
local_images_path = 'Images'
os.makedirs(local_images_path, exist_ok=True)

# Download images from Firebase Storage to the local directory
for blob in bucket.list_blobs(prefix=firebase_storage_path):
    blob_path = blob.name
    local_image_path = os.path.join(local_images_path, os.path.basename(blob_path))

    # Download image from Firebase Storage
    blob.download_to_filename(local_image_path)

print("Images downloaded and saved to the local 'images' directory with original file names")

folderPath= 'images'
pathList = os.listdir(folderPath)
#print(pathList)
imgList = []
familyIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))

    familyIds.append(os.path.splitext(path)[0])
   # print(os.path.splitext(path)[0])
print(familyIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, familyIds]
print(encodeListKnown)
print("Encoded")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds ,file)
file.close()