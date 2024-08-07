from lib2to3.pygram import pattern_symbols
import dlib
import cv2
import numpy as np
import csv
import datetime
import joblib
import schedule
import time
import threading
import pandas as pd
import csv
import mysql.connector

# 모델 파일 경로
model_filename = 'svm_model.pkl'

# 모델 불러오기
loaded_model = joblib.load(model_filename)

# dlib 랜드마크 모델 사용
detector = dlib.get_frontal_face_detector()
path = 'shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(path)


pupil_locate_list = [['date', 'time', 'right_eye_x', 'right_eye_y', 'left_eye_x', 'left_eye_y']]



def is_close(y0, y1):  # 눈이 감겼는지 판정하는 함수
    if abs(y0 - y1) < 10:
        return True
    return False


def get_center(gray_img):  # 이치화된 눈 화상에서 눈동자의 중심을 찾다
    moments = cv2.moments(gray_img, False)
    try:

        return int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])
    except:
        return None


def p(img, parts, eye):
    if eye[0]:
        cv2.circle(img, eye[0], 3, (255, 255, 0), -1)
    if eye[1]:
        cv2.circle(img, eye[1], 3, (255, 255, 0), -1)
    for i in parts:
        cv2.circle(img, (i.x, i.y), 3, (255, 0, 0), -1)

    cv2.imshow("me", img)


def get_eye_parts(parts, left=True):  # 눈 부분의 좌표를 구하다
    if left:
        eye_parts = [
            parts[36],
            min(parts[37], parts[38], key=lambda x: x.y),
            max(parts[40], parts[41], key=lambda x: x.y),
            parts[39],
        ]
    else:
        eye_parts = [
            parts[42],
            min(parts[43], parts[44], key=lambda x: x.y),
            max(parts[46], parts[47], key=lambda x: x.y),
            parts[45],
        ]
    return eye_parts


def get_eye_image(img, parts, left=True):  # 카메라 이미지와 찾은 얼굴 좌표에서 눈 이미지를 찾아 표시하다
    if left:
        eyes = get_eye_parts(parts, True)
    else:
        eyes = get_eye_parts(parts, False)
    org_x = eyes[0].x
    org_y = eyes[1].y

    if is_close(org_y, eyes[2].y):
        return None
    eye = img[org_y:eyes[2].y, org_x:eyes[-1].x]  # 이미지에서 눈동자 부분을 트리밍
    # img[top : bottom, left : right]
    # 파이썬 리스트: 마이너스 인덱스는 맨 끝에서 순서를 의미한다

    height = eye.shape[0]
    width = eye.shape[1]
    resize_eye = cv2.resize(eye, (int(width * 5.0), int(height * 5.0)))

    if left:
        cv2.imshow("left", resize_eye)
        cv2.moveWindow('left', 50, 200)
    else:
        cv2.imshow("right", resize_eye)
        cv2.moveWindow('right', 350, 200)

    return eye


def get_eye_center(img, parts, left=True):  # Parts에서 눈의 센터 위치를 찾아서 표시한다
    if left:
        eyes = get_eye_parts(parts, True)
    else:
        eyes = get_eye_parts(parts, False)

    x_center = int(eyes[0].x + (eyes[-1].x - eyes[0].x) / 2)
    y_center = int(eyes[1].y + (eyes[2].y - eyes[1].y) / 2)

    cv2.circle(img, (x_center, y_center), 3, (255, 255, 0), -1)
    return x_center, y_center


def get_pupil_location(img, parts, left=True):  # Parts에서 눈동자 위치를 찾아 표시하는 과정에서 눈의 이진화 이미지 표시
    if left:
        eyes = get_eye_parts(parts, True)  # 왼쪽 눈 부위의 좌표 가져오기
    else:
        eyes = get_eye_parts(parts, False)  # 오른쪽 눈 부위의 좌표 가져오기

    org_x = eyes[0].x  # 눈 부위 영상에서 원점의 x 좌표
    org_y = eyes[1].y  # 눈 부위 영상에서 원점의 y 좌표

    if is_close(org_y, eyes[2].y):
        return None  # 눈이 감겨있으면 None 반환

    expand_ratio = 1.0  # 확장 비율 설정
    height = eyes[2].y - org_y  # 눈 영상의 높이
    width = eyes[-1].x - org_x  # 눈 영상의 너비

    expand_height = int(height * (expand_ratio - 1) / 2)  # 높이에 대한 확장 크기
    expand_width = int(width * (expand_ratio - 1) / 2)  # 너비에 대한 확장 크기

    eye_start_y = max(0, org_y - expand_height)  # 확장된 눈 영상의 시작 y 좌표
    eye_end_y = min(img.shape[0], eyes[2].y + expand_height)  # 확장된 눈 영상의 끝 y 좌표
    eye_start_x = max(0, org_x - expand_width)  # 확장된 눈 영상의 시작 x 좌표
    eye_end_x = min(img.shape[1], eyes[-1].x + expand_width)  # 확장된 눈 영상의 끝 x 좌표

    eye = img[eye_start_y:eye_end_y, eye_start_x:eye_end_x]  # 눈 영상 확장하여 추출

    _, threshold_eye = cv2.threshold(cv2.cvtColor(eye, cv2.COLOR_RGB2GRAY),
    25,  # 임계값 설정
    255,  # 이진화 결과의 최대값
    cv2.THRESH_BINARY_INV)  # 눈 영상을 이진화

    height = threshold_eye.shape[0]  # 이진화된 눈 영상의 높이
    width = threshold_eye.shape[1]  # 이진화된 눈 영상의 너비

    resize_eye = cv2.resize(threshold_eye, (int(width * 5.0), int(height * 5.0)))  # 눈 영상 크기 조정

    if left:
        cv2.imshow("left_threshold", resize_eye)  # 왼쪽 눈 이진화된 영상 표시
        cv2.moveWindow('left_threshold', 50, 300)  # 왼쪽 눈 창 위치 이동
    else:
        cv2.imshow("right_threshold", resize_eye)  # 오른쪽 눈 이진화된 영상 표시
        cv2.moveWindow('right_threshold', 350, 300)  # 오른쪽 눈 창 위치 이동

    center = get_center(threshold_eye)  # 눈동자 중심 좌표 가져오기

    if center:
        cv2.circle(img, (center[0] + org_x, center[1] + org_y), 3, (255, 0, 0), -1)  # 이미지에 눈동자 중심 표시
        return center[0] + org_x, center[1] + org_y  # 눈동자 중심의 전체 이미지에서의 좌표 반환
    return center  # 눈동자 중심을 찾지 못한 경우 None 반환


def calculate_relative_pupil_position(img, eye_center, pupil_locate, left=True):  # e
    """
        눈의 중심 좌표와 눈동자 좌표에서 눈의 중앙에 대한 눈동자 상대 좌표를 구하는 함수입니다.

        Args:
            img: 분석 대상 이미지
            eye_center: 눈의 중심 좌표 (눈의 중앙을 기준으로 눈동자의 상대 위치를 계산하기 위함)
            pupil_locate: 눈동자 좌표
            left: 왼쪽 눈인지 여부 (기본값: True)

        Returns:
            relative_pupil_x: 눈동자의 중앙과의 상대적인 x 좌표
            relative_pupil_y: 눈동자의 중앙과의 상대적인 y 좌표
        """

    if not eye_center:
        return  # 눈의 중심 좌표가 없을 경우 함수 종료

    if not pupil_locate:
        return  # 눈동자 좌표가 없을 경우 함수 종료


    # 눈동자의 상대적인 x, y 좌표 계산
    relative_pupil_x = pupil_locate[0] - eye_center[0]
    relative_pupil_y = pupil_locate[1] - eye_center[1]

    if left:
        # 왼쪽 눈인 경우
        cv2.putText(img,
                    "left x=" + str(relative_pupil_x) + " y=" + str(relative_pupil_y),
                    org=(50, 400),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0, 255, 0),
                    thickness=2,
                    lineType=cv2.LINE_4)
    else:
        # 오른쪽 눈인 경우
        cv2.putText(img,
                    "right x=" + str(relative_pupil_x) + " y=" + str(relative_pupil_y),
                    org=(50, 450),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0, 255, 0),
                    thickness=2,
                    lineType=cv2.LINE_4)

    return relative_pupil_x, relative_pupil_y


def calculate_direction(img, parts, pupil_locate):  # 눈동자의 위치와 눈의 좌표에서 눈동자가 향하고 있는 방향을 찾아 표시하다
    if not pupil_locate:
        return

    eyes = get_eye_parts(parts, True)

    left_border = eyes[0].x + (eyes[3].x - eyes[0].x) / 3  # 눈을 좌우로 삼등분했을 때 왼쪽 영역의 경계선
    right_border = eyes[0].x + (eyes[3].x - eyes[0].x) * 2 / 3  # 눈을 좌우로 삼등분했을 때 오른쪽 영역의 경계선
    up_border = eyes[1].y + (eyes[2].y - eyes[1].y) / 3  # 눈을 위아래로 삼등분했을 때 상존의 경계선
    down_border = eyes[1].y + (eyes[2].y - eyes[1].y) * 2 / 3  # 눈을 위아래로 삼등분했을 때 아래 구역의 경계선

    if eyes[0].x <= pupil_locate[0] < left_border:
        # 눈동자는 왼쪽에 있다
        show_text(img, "LEFT", 50, 50)
    elif left_border <= pupil_locate[0] <= right_border:
        # 눈동자는 가운데에 있다
        show_text(img, "STRAIGHT", 50, 50)
    elif right_border <= pupil_locate[0] <= eyes[3].x:
        # 눈동자는 오른쪽에 있다
        show_text(img, "RIGHT", 50, 50)
    else:
        # 눈동자는 어디에도 없다
        show_text(img, "NONE", 50, 50)

    if pupil_locate[1] <= up_border:
        # 눈동자는 위에 있다
        show_text(img, "UP", 50, 100)
    elif up_border <= pupil_locate[1] <= down_border:
        # 눈동자는 중간 위치에 있다
        show_text(img, "MIDDLE", 50, 100)
    elif pupil_locate[1] >= down_border:
        # 눈동자는 아래 위치에 있다
        show_text(img, "DOWN", 50, 100)

    return


def show_text(img, text, x, y):
    cv2.putText(img,
                text,
                org=(x, y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0, 255, 0),
                thickness=2,
                lineType=cv2.LINE_4)
    return

def write_csv(data):  # list 받아서 pupil_locate.csv에 보냄
    if not data:
        return

    with open('pupil_locate.csv', 'w', newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerows(data)
        print("pupil_locate.csv")
    return


def append_pupil_locate_to_list(left_pupil_position, right_pupil_position):  # 현재 시각, 오른쪽 눈동자 위치, 왼쪽 눈동자 위치를 list에 추가한다

    # 왼쪽 눈동자 위치가 없는 경우, 함수 종료
    if not left_pupil_position:
        return

    # 오른쪽 눈동자 위치가 없는 경우, 함수 종료
    if not right_pupil_position:
        return

    # 현재 시각을 구한다
    for_write_time = datetime.datetime.now()

    # 현재 날짜, 시각, 왼쪽 눈동자 위치, 오른쪽 눈동자 위치를 리스트에 추가할 형식으로 정리한다
    locate = [
        datetime.date.today(),
        "{}:{}:{}".format(for_write_time.hour, for_write_time.minute, for_write_time.second),
        left_pupil_position[0], left_pupil_position[1], right_pupil_position[0], right_pupil_position[1]
    ]

    # pupil_locate_list에 위치 정보를 추가한다
    pupil_locate_list.append(locate)

    return


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    dets = detector(frame[:, :, ::-1])
    if len(dets) > 0:
        parts = predictor(frame, dets[0]).parts()

        left_eye_image = get_eye_image(frame, parts, True)
        right_eye_image = get_eye_image(frame, parts, False)
        left_eye_center = get_eye_center(frame, parts, True)
        right_eye_center = get_eye_center(frame, parts, False)
        left_pupil_location = get_pupil_location(frame, parts, True)
        right_pupil_location = get_pupil_location(frame, parts, False)
        left_relative_pupil_position = calculate_relative_pupil_position(frame, left_eye_center, left_pupil_location,
                                                                         True)
        right_relative_pupil_position = calculate_relative_pupil_position(frame, right_eye_center, right_pupil_location,
                                                                          False)
        calculate_direction(frame, parts, left_pupil_location)
        append_pupil_locate_to_list(left_relative_pupil_position, right_relative_pupil_position)
        cv2.imshow("Test", frame)

    key = cv2.waitKey(1)  # 1밀리초 키 입력을 기다리다

    if key == 27:  # Window를 선택하신 상태에서 ESC버튼을 누르면 꺼짐
        break
    elif key == ord('e'):  # E키가 눌리면 csv에 저장
        write_csv(pupil_locate_list)
    elif key == ord('a'):  # A키가 눌리면 AI시작
        def model():
            write_csv(pupil_locate_list)
            df = pd.read_csv('pupil_locate.csv')
            df.dropna(inplace=True)

            # 날짜와 시간을 하나의 datetime 열로 합칩니다.
            df['Datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

            # datetime 열을 인덱스로 설정합니다.
            df.set_index('Datetime', inplace=True)

            # 문자열 열 제거
            df = df[['right_eye_x', 'right_eye_y', 'left_eye_x', 'left_eye_y']].apply(pd.to_numeric, errors='coerce')

            # NaN 값이 있는 행 제거
            df.dropna(inplace=True)

            # 1 분 간격으로 데이터를 샘플링하고 x와 y 값을 계산합니다.
            df_resampled = df.resample('15S').mean()


            df_resampled['right_eye_x_movement'] = abs(df_resampled['right_eye_x'].diff())
            df_resampled['right_eye_y_movement'] = abs(df_resampled['right_eye_y'].diff())
            df_resampled['left_eye_x_movement'] = abs(df_resampled['left_eye_x'].diff())
            df_resampled['left_eye_y_movement'] = abs(df_resampled['left_eye_y'].diff())

            # 첫 번째 행의 이동량은 NaN으로 나타날 수 있으므로 0으로 대체
            df_resampled = df_resampled.fillna(0)

            movement_data = df_resampled[
                ['right_eye_x_movement', 'right_eye_y_movement', 'left_eye_x_movement', 'left_eye_y_movement']]


            # 모델에 movement 데이터 입력
            predicted_labels = loaded_model.predict(movement_data)

            print("집중도 판단 결과(0이면 집중 X , 1이면 집중 O)")
            # 분류 결과 출력
            print(predicted_labels)

            # 분류 결과를 df_resampled에 'target' 열로 저장
            df_resampled['target'] = predicted_labels


            # MySQL에 저장하기 전에 percent를 계산하고 열에 추가
            percent = [80]

            for label in predicted_labels:
                last_row = percent[-1]
                if label == 1:
                    if last_row < 100:
                        var = last_row + 1
                    elif last_row >= 100:
                        var = last_row
                elif label == 0:
                    if last_row > 0:
                        var = last_row - 1
                    elif last_row <= 0:
                        var = last_row

                percent.append(var)
            print("집중도 퍼센트")
            print(percent)
            percent.pop(0)
            df_resampled['percent'] = percent

            # MySQL 연결 정보
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'fhdlwp15',
                'database': 'test'
            }
            # MySQL 연결
            connection = mysql.connector.connect(**db_config)

            # 커서 생성
            cursor = connection.cursor()

            # 테이블 리셋하는 쿼리문
            reset_query = """
                TRUNCATE TABLE testtable
            """

            # 테이블 리셋 쿼리 실행
            cursor.execute(reset_query)

            # 데이터프레임을 MySQL 테이블에 삽입하는 쿼리문
            for index, row in df_resampled.iterrows():
                insert_query = f"""
                    INSERT INTO testtable 
                    VALUES ('{index}', {row['right_eye_x']}, {row['right_eye_y']}, {row['left_eye_x']}, {row['left_eye_y']},
                    {row['right_eye_x_movement']}, {row['right_eye_y_movement']}, {row['left_eye_x_movement']}, {row['left_eye_y_movement']},
                    {row['target']}, {row['percent']})
                """
                cursor.execute(insert_query)

            # 변경사항 커밋
            connection.commit()

            # 연결 종료
            cursor.close()
            connection.close()


        def schedule_task():
            while True:
                schedule.run_pending()
                time.sleep(1)


        schedule.every(15).seconds.do(model)
        schedule_thread = threading.Thread(target=schedule_task)
        schedule_thread.start()


cap.release()
cv2.destroyAllWindows()
