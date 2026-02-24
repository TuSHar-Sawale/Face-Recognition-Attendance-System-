# Face-Recognition-Attendance-System-
AI Face Recognition Attendance System (Supabase Integrated)

A real-time face recognition based attendance system that automatically identifies students using computer vision and updates attendance records directly in a Supabase database.

This system eliminates manual attendance, reduces proxy entries, and demonstrates end-to-end integration of computer vision with cloud backend infrastructure.

Backend implementation reference: 

main

#🚀 Problem Statement

Traditional attendance systems:

Are manual and time-consuming

Allow proxy attendance

Lack real-time database updates

This project solves that by using face recognition for automated, secure, and real-time attendance tracking.

#🧠 System Architecture

Webcam captures live video stream

Faces detected and encoded using face_recognition

Encodings compared with pre-trained known encodings

If matched:

Student data fetched from Supabase

Attendance validated using timestamp logic

Attendance incremented in database

Student profile image loaded from Supabase storage

Real-time UI overlay built using OpenCV + CvZone

#🛠 Tech Stack

Python

OpenCV

face_recognition (dlib-based embeddings)

NumPy

Supabase (PostgreSQL + Storage)

CvZone (UI overlay utilities)

Pickle (face encoding serialization)

#🔍 Core Features

Real-time face detection and recognition

Precomputed facial encodings for fast matching

Supabase PostgreSQL integration

Supabase Storage integration for student images

Attendance cooldown logic (prevents multiple entries within 30 seconds)

Dynamic UI with status modes (loading, success, duplicate detection)

Graceful shutdown and resource cleanup

Error handling for database and image fetch failures

#🧠 Technical Highlights
Face Matching Logic

Uses Euclidean distance between embeddings

Best match selected via np.argmin(face_distance)

Binary match validation using compare_faces

Attendance Validation Logic

Reads last_attendance_time

Calculates time delta

Updates only if cooldown threshold exceeded

Prevents duplicate attendance entries

Cloud Integration

Live student record fetch from Supabase

Secure storage retrieval for student images

Real-time attendance update via API

#📂 Project Structure
├── main.py
├── EncodeFile.p
├── Resources/
│   ├── background.png
│   └── Modes/
├── Supabase (Cloud)
│   ├── students table
│   └── student-images bucket
⚠ Security Notice

Supabase API keys should be stored in environment variables in production.
Current implementation is for demonstration purposes.

#📈 Future Improvements

Move API keys to environment variables

Convert to web-based system using Flask/FastAPI

Add liveness detection (anti-spoofing)

Deploy as institutional attendance SaaS

Add admin dashboard with analytics

Add logging system

Dockerize for production
