import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
import numpy as np, cv2
import matplotlib.pyplot as plt
import math
import random
import os
import re

from CtrlWindow import CtrlWindow 
from RgbFrame import RgbFrame
from SelectFrame import SelectFrame
from MouseObserver import MouseObserver
from SelState import SelState as ST

class Photoshop(QMainWindow):
    
    #전역변수 설정
    img_original  = np.zeros((3,3),np.uint8)#원본. 업데이트 안 함 
    img  = np.zeros((3,3),np.uint8)#현재 화면에 보여주는 이미지  
    prev_img = np.zeros((3,3),np.uint8)#적용 버튼 누르면 이미지 업데이트 todo

    img_list = []#undo, redo 함수 구현 todo 
    img_list_cnt = -1

    widget_cnt  = 0 
    focus_image_frame_flag = False #자식 마우스 이벤트 플래그

    select_flag = ST.NONE # 초기 상태.
    mouse_flag =ST.NONE # 마우스 누르지 않는 상태
    start_x, start_y = 0,0
    #rgb는 각 r,g,b 의 평균 값을 계산한거 !!!!
    rgb = [128, 128, 128]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     
        
        self.setMouseTracking(True)
        self.initUI()

    def initUI(self): 
        self.setWindowIcon(QtGui.QIcon('./img/cat.jpg'))#이미지
        self.setStyleSheet('background : lightgray;')
        self.setGeometry(250, 130, 1400, 850)    
        self.add_btn() #버튼 추가
        self.add_menubar()#메뉴바 추가
        self.setWindowTitle('PyQt5 포토샵 구현')#제목 설정
        self.layout = QVBoxLayout() #수직 레이아웃 설정
        self.setLayout(self.layout)

        self.add_widget(self.layout)
        self.show() #화면에 띄우기

    #버튼 추가
    def add_btn(self):
        #불러오기 버튼 
        img_path_btn = QPushButton('불러오기', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('이미지를 불러옵니다')
        img_path_btn.clicked.connect(self.openfile) #파일 불러오기 메소드
        img_path_btn.move(50, 50) #위치이동

        img_path_btn = QPushButton('원본 이미지 보기', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('이미지를 불러옵니다')
        img_path_btn.clicked.connect(self.show_img_original) #버튼 이벤트 처리 
        img_path_btn.move(150, 50) #위치이동

        img_path_btn = QPushButton('저 장', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('이미지를 저장합니다.')
        img_path_btn.clicked.connect(self.save_img) #버튼 이벤트 처리 
        img_path_btn.move(1200, 770) #가로, 세로
        
        img_path_btn = QPushButton('redo', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('실행 취소')
        img_path_btn.clicked.connect(self.redo) #버튼 이벤트 처리 
        img_path_btn.move(1000, 770) #가로, 세로
        
        img_path_btn = QPushButton('undo', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('재 실행')
        img_path_btn.clicked.connect(self.undo) #버튼 이벤트 처리 
        img_path_btn.move(1100, 770) #가로, 세로

    def add_widget(self,layout): # 위젯 추가
        #이미지 라벨 추가 .
        self.img_widget = ImageWidget(self,event_flag=True)
        
        #self.layout = QtWidgets.QFormLayout(self.img_widget)
        self.img_widget.setGeometry(100,100,700,700)#이미지 최대 크기 700 700
        self.ctrl_widget = CtrlWindow(self)
        self.ctrl_widget.setGeometry(900,130,250,470)
        
        self.rgb_frame = RgbFrame(self)
        self.rgb_frame.setGeometry(950,130,250,270)
        self.rgb_frame.hide()
        
        self.select_frame = SelectFrame(self)
        self.select_frame.setGeometry(950,130,250,270)
        self.select_frame.hide()

        layout.addWidget(self.img_widget)
        layout.addWidget(self.ctrl_widget)
        layout.addWidget(self.rgb_frame)
        layout.addWidget(self.select_frame)
        
    #메뉴바 추가
    def add_menubar(self):
        #키보드 이벤트 추가.
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Esc')#강제종료 키 esc
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        RedoAction = QAction('&Redo', self)
        RedoAction.setShortcut(QtGui.QKeySequence("Ctrl+Z"))#redo 키
        RedoAction.setStatusTip('되돌아가기')
        RedoAction.triggered.connect(self.redo)
        
        #상태바 추가
        self.add_statusbar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def closeEvent(self, event): #닫기 창 메시지박스 추가.
        quit_msg = "이미지 저장"
        reply = QMessageBox.question(self, '저장하시겠습니까?', quit_msg, QMessageBox.Yes, QMessageBox.No) #메시지박스

        if reply == QMessageBox.Yes:
            self.save_img()

        event.accept()

    def add_statusbar(self):#상태바 추가 
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def openfile(self): #파일 불러오기 파일을 불러옵니다. 
        file_name = QFileDialog.getOpenFileName(self, "파일 열기 . . .", "", "jpg 파일(*.jpg);;png 파일", "jpg 파일(*.jpg)") #파일 확장자명 설정
        #레이블에 띄웁니다. 
        #opencv 는 파일 입출력 할때 아스키 문자만 허용한다. 절대 경로사용 불가
        self.img_original = cv2.imdecode(np.fromfile(file_name[0], dtype=np.uint8),cv2.IMREAD_UNCHANGED)
        self.img = self.img_original.copy()
        self.prev_img = self.img_original.copy()
        self.img_list = []
        self.img_list_cnt = -1
        #rgb 평균값 할당.
        self.rgb = []
        a,b,c = cv2.split(self.img_original)
        self.rgb_2d_array =[c,b,a]

        mean_ch = cv2.mean(self.img)
        
        self.rgb.append(int(mean_ch[2]))
        self.rgb.append(int(mean_ch[1]))
        self.rgb.append(int(mean_ch[0]))
        
        self.display_img_widget(self.img) #이미지 업데이트
        print('이미지 위젯 좌표')
        print(self.img_widget.get_x(), self.img_widget.get_y())

        #self.ctrl_widget.update_rgb_label(rb = self.rgb)
        #self.ctrl_widget.init_track(self.rgb)

        if self.widget_cnt > 0:#도커 창 닫기
            dock.close()

    def save_img(self):
        if self.img is not None:
            img_file_path, _ = QFileDialog.getSaveFileName(self, "Save Image",
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;")
            if img_file_path and self.img is not None:
                print('저장진행')
                cv2.imwrite(img_file_path, self.img)
                if(re.search('.png',img_file_path)): #regex 로 문자 패턴 매칭 ~ 
                    is_success, im_buf_arr = cv2.imencode('.png',self.img) #opencv는 아스키코드 경로만 읽는다. 유니코드는 인코딩이 필요. 1차원 넘파이 배열로 변환한다. 
                else:
                    is_success, im_buf_arr = cv2.imencode('.jpg',self.img)
                im_buf_arr.tofile(img_file_path)
            else:
                QMessageBox.information(self, "Error", 
                    "Unable to save image.", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Empty Image", 
                    "There is no image to save.", QMessageBox.Ok)

    def show_img_original(self): #도킹 위젯에 원본 뛰우기 
        global dock
        self.widget_cnt = self.widget_cnt+1
        # dock 위젯 만든다.  
        dock = QDockWidget('원 본',self)
        img_dock_widget = ImageWidget(self)
        #img_widget.set_image(self.img_original) #원본으로 설정
        # adding widget to the layout
        dock.setWidget(img_dock_widget)
        dock.setGeometry(100, 100, 200, 200)
        dock.show()

    def focus_on(self):#이미지 프레임 포커싱 인  
        self.focus_image_frame_flag = True

    def focus_off(self):#이미지 프레임 포커싱 아웃
        self.focus_image_frame_flag = False
        self.statusBar().clearMessage() #포커싱 아웃될때 메시지 제거

    def savefile(self): #파일 저장하기 
        print('save file')

    def update_statusBar(self,a,b):
        tracking_location  = "마우스 좌표 (x,y) = ({0}, {1}), global x,y = {2},{3}".format(a.x(),a.y(),b.x(),b.y())
        self.statusBar().showMessage(tracking_location)
        
    #rgb는 각 rgb의 평균 값임 !
    def get_rgb(self):
        return self.rgb
    def get_r(self):
        return self.rgb[0]
    def get_g(self):
        return self.rgb[1]
    def get_b(self):
        return self.rgb[2]

    def add_img_list(self):#이미지 리스트 업데이트 메소드 
        self.prev_img = self.img 
        
        if self.img_list_cnt < 0 or len(self.img_list)-1 <= self.img_list_cnt:
            self.img_list.append(self.prev_img)
        else:
            self.img_list[self.img_list_cnt] = self.prev_img
        self.img_list_cnt += 1
        
    def display_img_widget(self,img):
        self.img_widget.set_image(img)

    ######################################## 시그널 연결 ########################3
    def handle_pressed(self, window_pos, global_pos): #마우스 좌표 저장 후 상태에 따라 연산실행. 
        self.mouse_flag = ST.LBUTTON_DOWN
        self.start_x = window_pos.x()
        self.start_y = window_pos.y()

    def handle_relase(self, window_pos, global_pos):
        x,y = window_pos.x(),window_pos.y()
        self.mouse_flag = ST.LBUTTON_UP
        self.roi_processing([self.start_x,self.start_y,x,y])
        self.select_Pos = [] #리스트 비웁니다.
        self.mouse_flag = ST.NONE

    def handle_moved(self, w_p, g_p):
        self.mouse_display(w_p)
        self.update_statusBar(w_p,g_p)
        if self.mouse_flag == ST.CUT: return #아무것도 안한다
        
        if self.mouse_flag == ST.LBUTTON_DOWN:#마우스 누른 상태에만. (블러닝, 샤프닝) 
            self.roi_processing(w_p)
        

    #####################################-----------############################3
#####################################################버튼 누르는 메소드 연결###################################
    #확인 버튼 클릭
    def click_ok(self):
        self.add_img_list()#메소드 호출
        #rgb 트랙바 숨김 이벤트 해제
        self.rgb_frame.hide()
        self.select_frame.hide()
        self.rgb_frame.close_trackbar()
        self.ctrl_widget.show()
        self.select_flag = ST.NONE #상태 초기화

    def click_cancle(self):
        #rgb 트랙바 숨김 이벤트 해제
        self.rgb_frame.hide()
        self.select_frame.hide()
        self.rgb_frame.close_trackbar()
        self.ctrl_widget.show()
        self.img = self.prev_img
        self.display_img_widget(self.img)
        self.select_flag = ST.NONE #상태 초기화

    def click_select(self):
        self.ctrl_widget.hide()
        self.select_frame.show()

    def click_blur(self):
        self.select_flag = ST.BLUR
    def click_cut(self):
        self.select_flag = ST.CUT
    def click_mosaic(self):
        self.select_flag = ST.MOSAIC
    def click_sharp(self):
        self.select_flag = ST.SHARP
    
    def click_resize(self):
        h, w = self.img.shape[:2]
        m = max(h,w)
        if m > 700:
            self.add_img_list
            if h > w:
                self.img = self.img_resize(self.img, height = 700)
            else :
                self.img = self.img_resize(self.img , width= 700)
            self.display_img_widget(self.img)

    def flip(self):
        self.add_img_list()#메소드 호출
        self.img = self.myflip(self.img)
        self.display_img_widget(self.img)
        self.click_ok()
        

    def rotate(self):
        self.add_img_list()#메소드 호출
        self.img = self.myrotate_90(self.img)
        self.display_img_widget(self.img)
        self.click_ok()
        
        
    #점묘법 필터 
    def filter_1(self):
        self.add_img_list()#메소드 호출
        self.img = self.pointillism_filter(self.img)
        self.display_img_widget(self.img)

    def filter_2(self):
        self.add_img_list()#메소드 호출
        self.img = self.pointillism_filter2(self.img)
        self.display_img_widget(self.img)

    def rgbtrack(self):
        self.rgb_frame.show()
        self.ctrl_widget.hide()
        #rgb 평균값 할당.
        self.rgb = []
        a,b,c = cv2.split(self.img)
        self.rgb_2d_array =[c,b,a]

        mean_ch = cv2.mean(self.img)
        
        self.rgb.append(int(mean_ch[2]))
        self.rgb.append(int(mean_ch[1]))
        self.rgb.append(int(mean_ch[0]))
        
        self.rgb_frame.init_track(self.rgb)

    #돌아가기    
    def redo(self): 
        if self.img_list_cnt == 0:
            self.img_list_cnt = -1
            self.img = self.img_original.copy()
            self.display_img_widget(self.img)

        elif self.img_list_cnt > 0:
            print(self.img_list_cnt)
            self.img_list_cnt -= 1
            self.img = self.img_list[self.img_list_cnt]
            self.display_img_widget(self.img)
    
    #재 실행    
    def undo(self):
        if self.img_list_cnt < len(self.img_list)-1 : 
            self.img = self.img_list[self.img_list_cnt]
            self.img_list_cnt += 1
            self.display_img_widget(self.img)

    #반전 필터
    def invert(self):
        self.add_img_list()#메소드 호출
        self.inversion()
    
    #현재 선택 상태에 따라 작업을 달리합니다. 
    def roi_processing(self,p):
        if self.select_flag == ST.NONE:
            pass
        elif self.select_flag == ST.CUT and self.mouse_flag == ST.LBUTTON_UP:
            self.cut(p)
        elif self.select_flag == ST.BLUR and self.mouse_flag == ST.LBUTTON_DOWN:
            self.blur(p)
        elif self.select_flag == ST.SHARP and self.mouse_flag == ST.LBUTTON_DOWN:
            self.sharp(p)
        elif self.select_flag == ST.MOSAIC and self.mouse_flag == ST.LBUTTON_DOWN:
            self.mosaic(p)

    def get_roi_pos(self,p):
        #(start_i, start_j)
        #(end_i, end_j)
        #총 4사분면 x -->방향   오른쪽방향 start_x < end_x 아래방향 start_y < end_y
        start_y,start_x = p[1]-100, p[0]-100
        end_y , end_x = p[3]-100, p[2]-100
        h, w = self.img.shape[:2]
        
        if start_x < 0 : start_x = 0
        if start_y < 0 : start_y = 0
        if end_x < 0 : end_x = 0
        if end_y < 0 : end_y = 0
        
        if start_x > w : start_x = w
        if end_x > w : end_x = w
        if start_y > h : start_y = h
        if end_y > h : end_y = h

        col , row = abs(start_x-end_x), abs(start_y-end_y)
        x1, y1, x2,y2 = start_x, start_y, end_x,end_y
        print(x1,y1,x2,y2)
        return min(x1,x2), min(y1,y2), col,row
        
        #return x1,y1,col,row #col, row 리턴

    def get_square_roi(self,p):
        #cv2.rectangle(img_back, (m_j-r//2,m_i-r//2),(m_j+r//2,m_i+r//2),(165,165,165),-1)
        x1,y1,x2,y2 = p.x()-112,p.y()-112,p.x()+12-100,p.y()+12-100 #saturate 방식으로 클립을 딴다.
        h, w = self.img.shape[:2]
        if x1 < 0 : x1 = 0
        if x2 < 0 : x2 = 0
        if y1 < 0 : y1 = 0
        if y2 < 0 : y2 = 0
        
        if x1 > w : x1 = w
        if x2 > w : x2 = w
        if y1 > h : y1 = h
        if y2 > h : y2 = h

        print(x1,y1,x2,y2)
        return x1,y1,x2,y2
#############################################-------------########################################################

############################################이미지 프로세싱#########################################################

    def blur(self,p):#클릭
        x1,y1,x2,y2 = self.get_square_roi(p)
        roi = self.img[y1:y2, x1:x2]   # 관심영역 지정
        roi = cv2.blur(roi, (25, 25)) # 블러(모자이크) 처리
        self.img[y1:y2, x1:x2] = roi   # 원본 이미지에 적용
        self.display_img_widget(self.img)

    def sharp(self,p):#클릭기준
        x1,y1,x2,y2 = self.get_square_roi(p)
        roi = self.img[y1:y2, x1:x2]   # 관심영역 지정
        kernel = np.array([[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1], [-1,-1,25,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]) #가운데 영역만 돋보이게 한다.
        kernel = np.full((7,7),-1)
        kernel[3][3] = 49
        if (roi is not None):
            roi = cv2.filter2D(roi, -1, kernel)#샤프닝 처리
            self.img[y1:y2, x1:x2] = roi
            self.display_img_widget(self.img)

    def cut(self,p):#네모 드래그 박스 기준
        if self.focus_image_frame_flag :#이미지 위에 있을 때만 
            print('cut 불림')
            x,y,w,h = self.get_roi_pos(p)
            if w > 0 and h > 0:
                if self.img_list_cnt == -1:
                    d_img = self.img_original[y:y+h, x:x+w].copy()
                else :
                    d_img = self.img_list[self.img_list_cnt][y:y+h, x:x+w].copy()
                print(x,y,w,h)# 74 33 131 116
                self.img = d_img
                self.display_img_widget(self.img)

    def inversion(self):
        self.img = 255 - self.img
        self.display_img_widget(self.img)

    #트랙바 rgb 연산
    def change_img_rgb(self,dif,rgb_flag):
        b,g,r = cv2.split(self.prev_img)

        if rgb_flag == 2:#Red
            r = cv2.add(r, dif)#연산을 한다. 
        elif rgb_flag ==1:#Green
            g = cv2.add(g , dif)
        elif rgb_flag ==0:#Blue
            b = cv2.add(b, dif)
        self.img = cv2.merge((r,g,b))

        self.display_img_widget(self.img)#화면에 띄웁니다.
        
    def update_rgb(self, rgb):
        self.rgb = rgb

    def update_image_rgb(self):
        im = cv2.merge(self.rgb_2d_array)
        self.display_img_widget(im)

    def myflip(self,img): #이미지 뒤집기
        i_len = len(img)
        j_len = len(img[0])
        img_flip = np.zeros_like(img)

        for i in range(i_len):
            for j in range(j_len):
                img_flip[i,j]  = img[i,j_len-j-1] #반대 위치의 픽셀 덮어씌운다. 
        return img_flip

    def myrotate_90(self,img): #이미지 90도 회전 
        img_rotate_quarter = np.zeros_like(img)
        i = len(img_rotate_quarter)
        j = len(img_rotate_quarter[0])
        #print('shape: {0} i : {1} j : {2} '.format(img_rotate_quarter.shape,i,j))
        img_rotate_quarter = img_rotate_quarter.reshape(j,i,-1)

        i = len(img_rotate_quarter)
        j = len(img_rotate_quarter[0])
        for j in range(len(img[0])):
            for i in range(len(img)):
                img_rotate_quarter[j,i] = img[i,j]
        a = self.myflip(img_rotate_quarter) #좌우반전
        return a

    #이미지 w, h 비율대로 resize 해서 왜곡을 피한다.
    #코드 사용 예 image = image_resize(image, height = 800)
    def img_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):#inter area는 cv2제공하는 양선형 보간법이다.
        if width is None and height is None:#widght, height 값이 없으면 연산 안 함.
            return image
        # 이미지 widght, height
        dim = None
        (h, w) = image.shape[:2]

        if width is None: # height 값을 파라미터로.
            r = height / float(h)
            dim = (int(w * r), height)
        else:           #width 값이 파라미터로 주어졌을때.
            r = width / float(w) # width 비율을 구하고 디멘션 생성
            dim = (width, int(h * r))

        #크기 재조정.
        resized = cv2.resize(image, dim, interpolation = inter)
        return resized

    #노이즈 뿌리는 함수
    def add_noise(self,img, noise_pixel):
        global weight
        print(noise_pixel)
        b,g,r = cv2.split(img)#rgb 분리
        rgb_list = [b,g,r]

        # img의 행 열을 가져온다.
        row , col = rgb_list[0].shape
        weight = int(math.sqrt(row * col // 40000)) #크기에 따른 노이즈 크기 조절
        if weight < 1 : weight =1
        # 노이즈 개수 지정
        number_of_pixels = 10000*weight
        #print(weight)
        for j in range(number_of_pixels):
            #랜덤 좌표에다 노이즈 부여
            y=random.randint(0, row - 1-weight)
            x=random.randint(0, col - 1-weight)
            
            for i in range(3):#rgb 위치는 동일
                div_img = rgb_list[i] #rgb 리스트 하나 불러온 다음  
                #div_img[y:y+2][x:x+2] = 255 #(255,255,255) 가중치 네모 사이즈 만큼 흰색 노이즈 뿌린다.
                for a in range(weight):
                    for b in range(weight):
                        div_img[y+a][x+b] = noise_pixel
        
        img = cv2.merge(rgb_list) #rgb 합침
        return img
    
    #점묘법 필터 함수
    def pointillism_filter(self,img):
        img_noise = self.add_noise(img.copy(),255)
        kernel = np.ones((3*weight+1,3*weight+1), np.uint8) / ((3*weight+1) * (3*weight+1) ) # 가중치에 따른 마스크 생성
        img_noise = cv2.erode(img_noise,kernel) #erode 연산으로 화이트 노이즈 없엠.
        return img_noise

    #밝은 점묘법 필터 함수
    def pointillism_filter2(self,img):
        img_noise = self.add_noise(img.copy(),0)# (0,0,0) 노이즈를 뿌린다.
        kernel = np.ones((3*weight+1,3*weight+1), np.uint8) / 9 # 가중치에 따른 마스크 생성
        img_noise = cv2.dilate(img_noise,kernel) #dilate 연산으로 객체 팽창.
        return img_noise

    def get_rgb(self):
        return self.rgb

    #화면에 마우스 위치 보여주는 UI
    def mouse_display(self,p,r=25):
        if self.img_original.sum() > 0 and self.focus_image_frame_flag :#이미지 위에 마우스 있을때만. 
            img = self.img.copy() 
            #마우스 (i,j) 좌표를 이미지 상의 좌표로 가져온다. 
            m_j,m_i = p.x()-100,p.y()-100
            # (100 100 700 700 ) geom           
            #   (100,100)  start   ()
            #
            #   (151,816)           (827,816)
            img_back = np.full_like(img,255) 
            if self.mouse_flag == ST.LBUTTON_DOWN:#클릭하면 네모로 바뀜.
                cv2.rectangle(img_back, (m_j-r//2,m_i-r//2),(m_j+r//2,m_i+r//2),(165,165,165),-1)
            else:
                cv2.circle(img_back, (m_j,m_i),r,(165,165,165),-1)

            img = cv2.bitwise_and(img_back, img)          #마우스 움직임에 따라 원 생성 and연산이기 때문에 제로 이미지 and하면 검은색 이미지가 생성된다. 
            self.img_widget.set_image(img,False)

#############################################----------------#########################################################

############################################이미지 위젯 클래스#########################################################
class ImageWidget(QtWidgets.QWidget):
    event_flag = False # 콜백 함수 실행 여부 플래그
    focus = False # 마우스 포커싱 실행 여부 
    def __init__(self, parent=None,event_flag = False):
        super(ImageWidget, self).__init__(parent)
        
       # self.setMouseTracking(True)
        self.image_frame = QLabel(self) #이미지 프레임 생성
        self.image = np.zeros((3,3),np.uint8)
        self.image_frame.enterEvent = self.enterEvent_2
        self.image_frame.leaveEvent = self.leaveEvent_2

        #self.layout = QVBoxLayout()
        #self.layout.addWidget(self.image_frame)
        #self.setLayout(self.layout)
        if parent is not None:
            self.set_image(parent.img_original)
        self.event_flag = event_flag #이벤트 플래그 설정
        self.parent = parent
        
    def set_image(self,img,flag = True): #이미지 변경
        h,w = img.shape[:2]
        self.image_frame.resize(w,h)
        #print(w,h)
        if flag :
            self.image = img
            self.show_image(self.image)
        else : 
            self.show_image(img)

    @pyqtSlot()
    def show_image(self,img): # Qimage 객체가 필요하다. 
        img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(img))

    def enterEvent_2(self, event): #들어온다.
        if self.event_flag :
            self.parent.focus_on()
            self.focus = True
        
    def leaveEvent_2(self, event): #마우스 포커싱 나갈때
        if self.event_flag :
            self.parent.focus_off()
            self.focus = False

    def get_focus(self):
        return self.focus

    def get_x(self):
        return self.image_frame.x()
    def get_y(self):
        return self.image_frame.y()

############################################--------------#########################################################

if __name__ == '__main__': #실행이 main함수인 경우
    app = QApplication(sys.argv)
    ex = Photoshop()
    mouse_observer = MouseObserver(ex.windowHandle())#마우스 이벤트 시그널 생성하는 클래스.
    mouse_observer.released.connect(ex.handle_relase)
    mouse_observer.pressed.connect(ex.handle_pressed)
    mouse_observer.moved.connect(ex.handle_moved)
    
    sys.exit(app.exec_())
