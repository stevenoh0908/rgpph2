'''
{Relationship between Galatic Physical Properties and H II Areas via its Image}
Date: 2020-06-07 Sun, KST
Developed by Stephen Oh, Chief Developer of Trendous Development Alliance & Studio.Chem with Ji-won Jang.
Email Address: stevenoh0908@gmail.com
> Warning
This Code uses numpy, opencv and matplotlib for execution, please make sure that you've installed them to your python's default directory via pip.
'''

import numpy as np
import cv2 as cv
import math
from matplotlib import pyplot as plt

class analysisManager():
    #Attribute
    BLOCK_SIZE = 3
    KERNEL_SIZE = 1
    EXPERICNCE = 0.04
    LOWER_RED = [0, 10, 10]
    UPPER_RED = [60, 255, 255] # 최적 H값은 실험 필요

    center_x = None
    center_y = None
    center_flag = False
    
    image = None
    grayImage = None
    hsvImage = None
    result_image = None
    
    starData = None
    start_x = None
    start_y = None
    end_x = None
    end_y = None

    circles = None
    excludeArea = None

    dst = None
    ret = None
    labels = None
    stats = None
    centroids = None

    mouse_is_pressing = False

    data = None

    def calculateDistance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)        

    def excludeLargeStars(self):
        self.circles = cv.HoughCircles(self.grayImage, cv.HOUGH_GRADIENT, 1, 100, param1 = 250, param2 = 10, minRadius = 1, maxRadius = 20)
        self.excludeArea = []
        for i in self.circles[0]:
            self.excludeArea.append([i[0] - i[2], i[1] - i[2], i[0] + i[2], i[1] + i[2]])
            #cv.circle(self.starData, (i[0], i[1]), i[2], (255, 0, 255), 3)
            pass
        
        for i in self.excludeArea:
            x1, y1, x2, y2 = i
            cv.rectangle(self.starData, (x1, y1), (x2, y2), (0,0,0), -1)
            pass
        #print(self.excludeArea)
        pass

    def drawDistancePlot(self):
        distance = []
        y = []
        for i in self.data:
            distance.append(i[2])
            y.append(0)
            pass

        plt.plot(distance, y, 'r.')
        plt.show()
        pass
        
    def harrisCorner(self):
        self.data = []
        self.grayImage = np.float32(self.grayImage) 
        self.dst = cv.cornerHarris(self.grayImage, self.BLOCK_SIZE, self.KERNEL_SIZE, self.EXPERICNCE) #조정 필요
        self.dst = cv.dilate(self.dst, None)
        self.ret, self.dst = cv.threshold(self.dst, 0.01*self.dst.max(), 255, 0) #Adjustion 계수의 의미?
        self.dst = np.uint8(self.dst)

        self.ret, self.labels, self.stats, self.centroids =  cv.connectedComponentsWithStats(self.dst)

        cnt=0

        for i in range(self.ret):
            if i<1:
                continue
            
            area = self.stats[i, cv.CC_STAT_AREA]
            left = self.stats[i, cv.CC_STAT_LEFT]
            top = self.stats[i, cv.CC_STAT_TOP]
            center_x = int(self.centroids[i, 0])
            center_y = int(self.centroids[i, 1])
        
            flag = False
            offset = 3
            for item in self.excludeArea:
                x1, y1, x2, y2 = item
                if x1 - offset <= center_x <= x2 + offset and y1-offset <= center_y <= y2+offset:
                    #print(i)
                    flag = True
                    pass
                pass

            if flag:
                continue
            
            if not (self.LOWER_RED[0] <= self.hsvImage[center_y][center_x][0] <= self.UPPER_RED[0] and self.LOWER_RED[1] <= self.hsvImage[center_y][center_x][1] <= self.UPPER_RED[1] and self.LOWER_RED[2] <= self.hsvImage[center_y][center_x][2] <= self.UPPER_RED[2]):
                continue
           
            if area>2:
                cv.putText(self.starData,str(i), (left + 20, top+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                cnt+=1
                pass
            cv.circle(self.starData, (center_x, center_y), 2, (0, 255, 255), 3)

            distance = self.calculateDistance(center_x, center_y, self.center_x, self.center_y)
            self.data.append([center_x, center_y, distance, area])
            #cv.imwrite('test5.jpg', self.starData)
            #cv.circle(self.hsvImage, (center_x, center_y), 2, (0, 255,255), 3)
            pass
        
        #self.starData[self.dst>0.01*self.dst.max()]=[0,0,255]
        #self.result_image[self.start_y:self.end_y, self.start_x:self.end_x] = self.starData
        '''
        for line in self.centroids:
            x = int(line[0])
            y = int(line[1])
            print((x, y))
            cv.circle(self.starData, (x, y), 2, (0, 255, 255), 3)
            pass
        '''
        cv.imshow("img_color",self.starData)
        #cv.imshow('img_hsv', self.hsvImage)

        self.drawDistancePlot()
        pass
    pass

    def cropArea(self):
        self.starData = self.image[self.start_y:self.end_y, self.start_x:self.end_x]
        pass

    def mouseCallBack(self, event, x, y, flags, param):
            self.result_image = self.image.copy()
            if not self.center_flag and event == cv.EVENT_RBUTTONDOWN:
                self.center_x, self.center_y = x, y
                cv.circle(self.result_image, (x, y), 5, (255, 0, 0),-1)
                cv.imshow('img_color', self.result_image)
                self.center_flag = True
                return
            if event == cv.EVENT_LBUTTONDOWN:
                self.mouse_is_pressing = True
                self.start_x, self.start_y = x, y
                cv.circle(self.result_image, (x, y), 10, (0, 255, 0), -1)
                cv.imshow('img_color', self.result_image)
                pass
            elif event == cv.EVENT_MOUSEMOVE:
                if self.mouse_is_pressing:
                    cv.rectangle(self.result_image, (self.start_x, self.start_y), (x, y), (0,255,0), 3)
                    cv.imshow('img_color', self.result_image)
                    pass
                pass
            elif event == cv.EVENT_LBUTTONUP:
                self.mouse_is_pressing = False
                self.end_x, self.end_y = x,y
                self.cropArea()
                self.grayImage = cv.cvtColor(self.starData, cv.COLOR_BGR2GRAY)
                self.hsvImage = cv.cvtColor(self.starData, cv.COLOR_BGR2HSV)
                self.excludeLargeStars()
                self.harrisCorner()
                pass
            pass

    def __init__(self, imageDir):
        self.image = cv.imread(imageDir, cv.IMREAD_COLOR)
        cv.imshow("img_color", self.image)
        cv.setMouseCallback("img_color", self.mouseCallBack)
        cv.waitKey(0)
        cv.destroyAllWindows()
        pass

    pass

if __name__ == '__main__':
    #print("탐색할 이미지의 이름을 입력: ")
    #imageDir = str(input())
    imageDir = 'croped.tif'
    analysismanager = analysisManager(imageDir)
    pass


    
