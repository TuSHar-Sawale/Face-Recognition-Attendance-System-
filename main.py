import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from supabase import create_client
from datetime import datetime
import time
import signal
import sys

SUPABASE_URL = "https://ksfqvefeqhrnqutnkpxo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzZnF2ZWZlcWhybnF1dG5rcHhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc2Mzc0MjYsImV4cCI6MjA2MzIxMzQyNn0.nylC--UMAYovLgXa5BsxHwY9_8i4Pa9C6xZ7H8bOYDU"

def cleanup(cap):
    print("\nCleaning up resources...")
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

def signal_handler(sig, frame):
    print('\nCtrl+C detected. Performing cleanup...')
    cleanup(cap)
    sys.exit(0)

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Failed to open camera")
    cap.set(3, 640)
    cap.set(4, 480)
    return cap

def load_resources():
    imgBackground = cv2.imread('Resources/background.png')
    if imgBackground is None:
        raise FileNotFoundError("Background image not found")

    folderModePath = 'Resources/Modes'
    modePathList = os.listdir(folderModePath)
    imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]
    return imgBackground, imgModeList

try:
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    cap = initialize_camera()
    imgBackground, imgModeList = load_resources()

    print("Loading Encode File ...")
    with open('EncodeFile.p', 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode File Loaded")

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera")
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]

                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

            if counter != 0:
                if counter == 1:
                    # Get student info from Supabase
                    try:
                        studentInfo = supabase.table("students").select("*").eq("id", id).execute().data[0]
                    except Exception as e:
                        print(f"Error fetching student info for id {id}: {e}")
                        continue  # Skip to the next iteration if student info is not found

                    # Get student image from Supabase storage
                    try:
                        response = supabase.storage.from_("student-images").download(f"{id}.png")
                        image_data = response.content if hasattr(response, "content") else response
                        nparr = np.frombuffer(image_data, np.uint8)
                        imgStudent = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if imgStudent is None:
                            raise ValueError("Image decoding failed")
                    except Exception as e:
                        print(f"Could not load image for student {id}: {e}")
                        imgStudent = np.zeros((216, 216, 3), np.uint8)


                    # Check attendance timing
                    try:
                        last_attendance = datetime.strptime(studentInfo['last_attendance_time'].replace('T', ' ')[:19],
                                                            "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - last_attendance).total_seconds()

                        if secondsElapsed > 30:
                            try:
                                supabase.table("students").update({
                                    "total_attendance": studentInfo['total_attendance'] + 1,
                                    "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }).eq("id", id).execute()
                            except Exception as e:
                                print(f"Error updating attendance for id {id}: {e}")
                                continue
                        else:
                            modeType = 3
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    except ValueError as ve:
                        print(f"Error parsing last_attendance_time for id {id}: {ve}")
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


                if modeType != 3:
                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        if imgStudent is not None and imgStudent.size > 0:
                            imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        time.sleep(2)  # Delay added here before clearing info
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

        cv2.imshow("Face Attendance", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Add 'q' key to quit
            break

except KeyboardInterrupt:
    print("\nProgram interrupted by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cleanup(cap)