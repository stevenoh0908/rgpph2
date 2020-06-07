#허프 원 변환 알고리즘 테스트
import cv2 as cv

src = cv.imread('croped.tif')
dst = src.copy()
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 100, param1 = 200, param2 = 10, minRadius = 30, maxRadius = 40)

for i in circles[0]:
    cv.circle(dst, (i[0], i[1]), i[2], (0, 255, 255), 3)
    pass

cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()
