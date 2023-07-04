# -*- coding: utf-8 -*-
"""
"""

pip install opencv-python

pip install mediapipe --user

pip install pygame

import cv2
import mediapipe as mp
import random
from pygame import mixer

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

mixer.init()
mixer.music.load('music1.mp3')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
w = 540
h = 320
score = 0

districts = [
    [(0, 0), (w // 2, h // 2)],
    [(w // 2, 0), (w, h // 2)],
    [(0, h // 2), (w // 2, h)],
    [(w // 2, h // 2), (w, h)]
]

adjust_interval = 3
last_adjust_time = 0

overlay_alpha = 0.3
overlay_color = (0, 0, 255, 76)  # 透明度為30%

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    run = True
    district = random.randint(0, 3)
    while True:
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        img = cv2.resize(img, (w, h))
        size = img.shape
        w = size[1]
        h = size[0]

        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        if current_time - last_adjust_time >= adjust_interval:
            last_adjust_time = current_time
            district = random.randint(0, 3)

        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img2)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = hand_landmarks.landmark[7].x * w
                y = hand_landmarks.landmark[7].y * h
                print(x, y)
                if district >= 0 and 0 < x < w and 0 < y < h:
                    rect_start, rect_end = districts[district]
                    rect_x_start, rect_y_start = rect_start
                    rect_x_end, rect_y_end = rect_end
                    if rect_x_start < x < rect_x_end and rect_y_start < y < rect_y_end:
                        run = True
                        score += 1
                        if not mixer.music.get_busy():
                            mixer.music.play()

                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        rect_start, rect_end = districts[district]
        rect_x_start, rect_y_start = rect_start
        rect_x_end, rect_y_end = rect_end

        overlay = img.copy()
        overlay = cv2.rectangle(overlay, rect_start, rect_end, overlay_color, -1)
        img = cv2.addWeighted(overlay, overlay_alpha, img, 1 - overlay_alpha, 0)

        cv2.putText(img, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(5) == ord('q'):
            break

mixer.music.stop()

cap.release()
cv2.destroyAllWindows()



