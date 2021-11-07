import cv2
import mediapipe as mp
import socket

sender = True
if sender:
    s = socket.socket()
    hostname = socket.gethostname()
    port = 5050
    s.connect((hostname, port))

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

while True:

    success, image = cap.read()
    width, height, _ = image.shape
    image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_RGB)

    try:
        nose = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * width), int(
            results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * height)
    except:
        nose = (int(width / 2), int(height / 2))

    nose_error = nose[0] - int(width / 2), nose[1] - int(height / 2)
    if sender:
        s.send(str(nose_error).encode())
    cv2.line(image, (int(height / 2), 0), (int(height / 2), width), (208, 224, 64), 1)
    cv2.line(image, (0, int(width / 2)), (height, int(width / 2)), (208, 224, 64), 1)
    cv2.imshow("Frame", cv2.flip(image, 1))
    cv2.waitKey(1)
