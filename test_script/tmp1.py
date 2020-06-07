import cv2 as cv
import numpy as np

lower_red = np.array([0, 10, 10])
upper_red = np.array([20, 255, 255])

def mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(image[y][x])
        print(hsv[y][x])
        pass

image = cv.imread('croped.tif', cv.IMREAD_COLOR)
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
cv.imshow('img_color', image)

mask = cv.inRange(hsv, lower_red, upper_red)
res = cv.bitwise_and(image, image, mask=mask)

cv.imshow('img_masked', res)

bgr_red = np.uint8([[[0, 0, 255]]])
hsv_red = cv.cvtColor(bgr_red, cv.COLOR_BGR2HSV)
print(hsv_red)

cv.setMouseCallback('img_color', mouse)
cv.waitKey(0)
cv.destroyAllWindows()
