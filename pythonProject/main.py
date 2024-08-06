import cv2
import dlib
import numpy as np

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식
    faces = detector(gray)

    # 인식된 얼굴에 대해 눈동자 검출
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = []
        right_eye = []

        # 눈의 좌표 구하기
        for n in range(36, 42):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            left_eye.append((x, y))
        for n in range(42, 48):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            right_eye.append((x, y))

        # 눈 영역 그리기
        left_eye = np.array(left_eye, np.int32)
        right_eye = np.array(right_eye, np.int32)
        cv2.polylines(frame, [left_eye], True, (0, 255, 255), 2)
        cv2.polylines(frame, [right_eye], True, (0, 255, 255), 2)

        # 눈동자 검출
        left_pupil = cv2.convexHull(left_eye)
        right_pupil = cv2.convexHull(right_eye)

        # 눈동자 중심 좌표 찾기
        left_eye_center = np.mean(left_eye, axis=0).astype(int)
        right_eye_center = np.mean(right_eye, axis=0).astype(int)

        # 눈동자 그리기
        cv2.circle(frame, tuple(left_eye_center), 3, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_eye_center), 3, (0, 0, 255), -1)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
1