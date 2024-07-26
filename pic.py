# Вырезает кусок изображения в другое изображения
import cv2
import os

img0 = cv2.imread('./data/road-signs/footpath.jpg')
cv2.imshow('img0', img0)

print('Введи первую координату:')
x1, y1 = input().split(' ')
print('Введи вторую координату:')
x2, y2 = input().split(' ')
x1 = int(x1)
x2 = int(x2)
y1 = int(y1)
y2 = int(y2)

img1 = img0[x1:x2, y1:y2]
cv2.imshow('img1', img1)


while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
