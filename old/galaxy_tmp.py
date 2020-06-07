import numpy as np
import cv2 as cv
import math

class analysisManager():

    #Attribute
    BLOCK_SIZE = 3
    KERNEL_SIZE = 1
    EXPERICNCE = 0.04    
    
    image = None
    grayImage = None
    result_image = None
    starData = None
    start_x = None
    start_y = None
    end_x = None
    end_y = None

    dst = None
    ret = None
    labels = None
    stats = None
    centroids = None

    mouse_is_pressing = False

    def harrisCorner(self):
        self.grayImage = cv.cvtColor(self.starData, cv.COLOR_BGR2GRAY)
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

            if area>2:
                cv.putText(self.starData,str(i), (left + 20, top+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                cnt+=1
                pass
            pass

        print(self.centroids)
        print(self.ret)
        self.starData[self.dst>0.01*self.dst.max()]=[0,0,255]
       # self.result_image[self.start_y:self.end_y, self.start_x:self.end_x] = self.starData
        for line in self.centroids:
            x = int(line[0])
            y = int(line[1])
            print((x, y))
            cv.circle(self.starData, (x, y), 2, (0, 255, 255), 3)
            pass
        cv.imshow("img_color",self.starData)
        pass
    pass

    def cropArea(self):
        self.starData = self.image[self.start_y:self.end_y, self.start_x:self.end_x]
        pass

    def mouseCallBack(self, event, x, y, flags, param):
            self.result_image = self.image.copy()
            
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
                self.harrisCorner()
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
    print("탐색할 이미지의 이름을 입력: ")
    imageDir = str(input())
    analysismanager = analysisManager(imageDir)
    pass


    
