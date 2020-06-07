import numpy as np
import cv2 as cv
import math
import tkinter as tk

mouse_is_pressing = False
start_x, start_y = -1, -1
Nf=[]
G=[]
def distance(x1,y1,x2,y2):
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return float("{0:.4f}".format(d))

match_rate=[]
def Search(name,count):
    global match_rate
    f_name=name+'.txt'
    f=open(f_name,'r')
    cnt=int(f.readline())

    data=[]
    Sn=[]
    
    for i in range(cnt):
        data.append(f.readline())
        data[i]=data[i].split(" ")
        Sn.append(int(data[i][0]))
        data[i]=list(map(float,data[i][1].split(",")))
    
    f.close()
    idx=namelist.index(name)
    
    C=0
    E=0
    for i in range(count):
        for j in range(cnt):
            correction=0
            for k in range(cnt):
                E=G[i]-data[j][k]
                if(-1<E<1):
                    correction+=1
            if(correction/cnt*100>70):
                C+=1
    match_rate.append(float("{0:.5f}".format((C/cnt)*100)))
    #print('correction:',C)
    print(name,match_rate[idx],sep=':')
    
   

def txtbox():
    win=tk.Tk()
    win.title("알림")
    win.geometry('200x100+200+200')
    num=tk.Entry(win,width=10)
    num.grid(column=0,row=0)
    def clk():
        global star
        star=int(num.get())
        print('star number of finding center:',star)
        win.destroy()
    act=tk.Button(win,text='확인',command=clk)
    act.grid(column=0,row=1)
    num.bind("<Return>", clk)
    win.mainloop()
    
def mouse_callback(event, x, y, flags, param):
    global start_x, start_y,last_x,last_y,mouse_is_pressing,d,centroids,G,ct
    
    
    img_result = img_color.copy()

    if event == cv.EVENT_LBUTTONDOWN:

        mouse_is_pressing = True
        start_x, start_y = x, y

        cv.circle(img_result, (x,y), 10, (0, 255, 0), -1)

        cv.imshow("img_color", img_result)

    elif event == cv.EVENT_MOUSEMOVE:

        if mouse_is_pressing:
            cv.rectangle(img_result, (start_x, start_y), (x, y), (0, 255, 0), 3)

            cv.imshow("img_color", img_result)

    elif event == cv.EVENT_LBUTTONUP:

        mouse_is_pressing = False

        last_x,last_y=x,y
        
        img_stars = img_color[start_y:y, start_x:x]
      
        gray = cv.cvtColor(img_stars,cv.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv.cornerHarris(gray, 2, 3, 0.04)

        dst = cv.dilate(dst,None)
        ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)

        dst=np.uint8(dst)

        ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)

        cnt=0

        for i in range(ret):

            if i<1:
                continue
            area = stats[i, cv.CC_STAT_AREA]
            left = stats[i, cv.CC_STAT_LEFT]
            top = stats[i, cv.CC_STAT_TOP]
            center_x = int(centroids[i, 0])
            center_y = int(centroids[i, 1])

            if area>2:
                cv.putText(img_stars,str(i), (left + 20, top+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                cnt+=1
                Nf.append(i)
                
        img_stars[dst>0.01*dst.max()]=[0,0,255]

        img_result[start_y:y, start_x:x] =img_stars
        
        cv.imshow("img_color",img_color)
        
        H,W,Ch=img_stars.shape
        k=24500000 #Calibration constant
        d=cnt*k/(H*W)

        txtbox()
        cv.destroyAllWindows()
        
        cv.imshow("dst",img_stars)
        
        star_x=int(centroids[star,0])
        star_y=int(centroids[star,1])

        hf=int(d/2)
        x1=star_x - hf
        x2=star_x + hf
        y1=int(star_y +(H/W)* hf)
        y2=int(star_y - (H/W)*hf)
        
        cv.rectangle(img_stars, (x1,y1),(x2,y2) ,(0,255,0),3)
        
        ct=0

        for j in Nf :
            if(x1<centroids[j,0]<x2 and y2<centroids[j,1]<y1):
                nearby_x=int(centroids[j,0])
                nearby_y=int(centroids[j,1])
                ct+=1
                
                G.append(distance(star_x,star_y,nearby_x,nearby_y))
        cv.imshow("result",img_stars)
        
        if(0 in G):
            l=G.copy()
            l.remove(0)
            ct=ct-1
        k=min(l)
        for i in range(ct):
            G[i]/=k
            G[i]=float("{0:.2f}".format(G[i]))

        for name in namelist:
            Search(name,ct)
    
        Find=max(match_rate)
        F_index=match_rate.index(Find)
        F_name=namelist[match_rate.index(Find)]
        for i in range(50):
            print('-',end='')
        print('\n')
        print(F_name,":",Find,"%")
        
        
namelist=['AUR','CAS','CEP','CYG','GEM','HER','LYR','ORI','PEG','TAU','UMI']

Filename=input('탐색할 이미지의 이름을 입력해 주세요:')
img_color = cv.imread(Filename, cv.IMREAD_COLOR )

cv.imshow("img_color", img_color)
cv.setMouseCallback('img_color', mouse_callback)
    
cv.waitKey(0)
cv.destroyAllWindows()
