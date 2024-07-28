import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')

ranges = {
    'min_h1': {'current': 32, 'max': 180},
    'max_h1': {'current': 70, 'max': 180},
}
     

def trackbar_handler(name):
    def handler(x):
        global ranges
        ranges[name]['current'] = x

    return handler


for name in ranges:
    cv2.createTrackbar(name, 'result', ranges[name]['current'], ranges[name]['max'], trackbar_handler(name))

while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    min_ = (ranges['min_h1']['current'], 0, 0)
    max_ = (ranges['max_h1']['current'], 255, 255)

    mask = cv2.inRange(frame, min_, max_)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('result', result)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
