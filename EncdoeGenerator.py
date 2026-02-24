import cv2
import face_recognition
import pickle
import os
from supabase import create_client

SUPABASE_URL = "https://ksfqvefeqhrnqutnkpxo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzZnF2ZWZlcWhybnF1dG5rcHhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc2Mzc0MjYsImV4cCI6MjA2MzIxMzQyNn0.nylC--UMAYovLgXa5BsxHwY9_8i4Pa9C6xZ7H8bOYDU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = [cv2.imread(os.path.join(folderPath, path)) for path in pathList]
studentIds = [os.path.splitext(path)[0] for path in pathList]

def findEncodings(imagesList):
    return [face_recognition.face_encodings(img)[0] for img in imagesList]

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print(encodeListKnown)
print("Encoding Complete")
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("File Saved")
