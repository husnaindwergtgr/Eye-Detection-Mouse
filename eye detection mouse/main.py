import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize MediaPipe Drawing Utility
mp_drawing = mp.solutions.drawing_utils

# Initialize OpenCV Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    # Convert the BGR image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find faces
    results = face_detection.process(image)

    # Convert the image color back so it can be displayed
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.detections:
        for detection in results.detections:
            # Draw face detections
            mp_drawing.draw_detection(image, detection)

            # Get the landmarks/parts for the face in box (the eyes)
            for id, lm in enumerate(detection.location_data.relative_keypoints):
                h, w, c = image.shape
                # Only consider landmarks that correspond to the eyes (ids 0 and 1)
                if id == 0 or id == 1:
                    x, y = int(lm.x * w), int(lm.y * h)
                    # Simulate mouse events based on eye landmarks
                    if id == 0:  # Left eye corresponds to mouse click
                        pyautogui.click()
                    elif id == 1:  # Right eye corresponds to mouse movement
                        pyautogui.moveTo(x, y)

    # Display the image
    cv2.imshow('MediaPipe Face Detection', image)

    if cv2.waitKey(1) & 0xFF == ord('?'):
        break

cap.release()
cv2.destroyAllWindows()
