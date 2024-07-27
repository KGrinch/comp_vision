import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')


while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    '''frame_h = frame_hsv[:, :, 0]
    frame_s = frame_hsv[:, :, 1]
    frame_v = frame_hsv[:, :, 2]'''

    min_1 = (0, 0, 0)
    max_1 = (15, 255, 255)
    min_2 = (170, 0, 0)
    max_2 = (180, 255, 255)

    mask1 = cv2.inRange(frame, min_1, max_1)
    # mask2 = cv2.inRange(frame, min_2, max_2)

    result = cv2.bitwise_and(frame, frame, mask=mask1)

    cv2.imshow('mask', mask1)
    cv2.imshow('result', result)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
