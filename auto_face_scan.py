import cv2
import time

face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("🎥 Starting automatic face scan...")

face_detected = False
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_detected = True
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_img = frame[y:y+h, x:x+w]
        cv2.imwrite("face_capture.jpg", face_img)
        print("✅ Face captured and saved as face_capture.jpg")
        break

    cv2.imshow("Auto Face Scan", frame)

    if face_detected or (time.time() - start_time > 10):
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
