import pyautogui
import time
import numpy as np
import cv2
import keyboard_emu as kbe
from threads_kbe import steer
from threading import Thread
# import imutils
# from path_finder import green_detector

# Ждем три секунды, успеваем переключиться на окно:
print('waiting for 2 seconds...')
time.sleep(2)

# ВНИМАНИЕ! PyAutoGUI НЕ ЧИТАЕТ В JPG!
title = './title.png'

nfs_window_location = None
searching_attempt = 1
while searching_attempt <= 5:
    nfs_window_location = pyautogui.locateOnScreen(title)

    if nfs_window_location is not None:
        print('nfs_window_location = ', nfs_window_location)
        break
    else:
        searching_attempt += 1
        time.sleep(1)
        print("attempt %d..." % searching_attempt)

if nfs_window_location is None:
    print('NFS Window not found')
    exit(1)


# Извлекаем из картинки-скриншота только данные окна NFS.
# Наша target-картинка - это заголовочная полоска окна.
# Для получения скриншота, мы берем ее левую точку (0),
# а к верхней (1) прибавляем высоту (3)
left = int(nfs_window_location[0])
top = int(nfs_window_location[1]+nfs_window_location[3])

# Здесь надо выставить те параметры, которые вы задали в игре.
window_resolution = (630, 480)

window = (left, top, left+window_resolution[0], top+window_resolution[1])

cv2.namedWindow('result')

loc = None


def my_loc():
    global loc
    return loc


th = Thread(target=steer, args=(my_loc,))
th.start()

ranges = {
    'min_h': {'current': 59, 'max': 180},
    'max_h': {'current': 67, 'max': 180},
    'min_s': {'current': 110, 'max': 180},
    'max_s': {'current': 180, 'max': 180},
    'min_v': {'current': 47, 'max': 180},
    'max_v': {'current': 180, 'max': 180}
}


def trackbar_handler(item):
    def handler(x):
        global ranges
        ranges[item]['current'] = x

    return handler


for name in ranges:
    cv2.createTrackbar(name, 'result', ranges[name]['current'], ranges[name]['max'], trackbar_handler(name))

while True:
    # print((left, top, window_resolution[0], window_resolution[1]))
    pix = pyautogui.screenshot(region=(left, top, window_resolution[0], window_resolution[1]))
    num_pix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)
    num_pix = cv2.cvtColor(num_pix, cv2.COLOR_BGR2HSV)
    num_pix = num_pix[window_resolution[1]//2:, :, :]

    min_ = (ranges['min_h']['current'], ranges['min_s']['current'], ranges['min_v']['current'])
    max_ = (ranges['max_h']['current'], ranges['max_s']['current'], ranges['max_v']['current'])

    mask = cv2.inRange(num_pix, min_, max_)
    result = cv2.bitwise_and(num_pix, num_pix, mask=mask)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    contours = contours[0]

    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        cv2.drawContours(result, contours, 0, (255, 0, 0), 1)
        cv2.drawContours(result, contours, 0, (255, 255, 255), 1)

        for idx, c in enumerate(contours):

            (x, y, w, h) = cv2.boundingRect(contours[idx])
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 1)

            center_x = (x + w//2)
            center_y = (y + h//2)

            cv2.line(result, (315, 480), (center_x, center_y), (255, 255, 255), 1)

            loc = center_x - (window_resolution[1] // 2)

            # func(loc)

    cv2.imshow('result', result)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
