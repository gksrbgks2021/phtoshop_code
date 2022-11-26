import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
import numpy as np, cv2
import matplotlib.pyplot as plt
import math
import random
import os

from CtrlWindow import CtrlWindow 

class Photoshop(QMainWindow):
    #전역변수 설정
    img_original  = np.zeros((3,3),np.uint8)
    img  = np.zeros((3,3),np.uint8)
    img_list = []
    widget_cnt = 0
    focus_image_frame_flag = False #자식 마우스 이벤트 플래그
    
    #이미지 값 조정
    rgb = [128, 128, 128]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      
        self.setMouseTracking(True)
        self.initUI()
        
    def initUI(self): 
        self.setWindowIcon(QtGui.QIcon('./img/cat.jpg'))#이미지
        self.setStyleSheet('background : lightgray;')
        self.setGeometry(250, 130, 1300, 850)    
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
        img_path_btn.setToolTip('이미지를 불러옵니다')
        img_path_btn.clicked.connect(self.save_img) #버튼 이벤트 처리 
        img_path_btn.move(1200, 770) #가로, 세로
    
    def add_widget(self,layout): # 위젯 추가
        self.img_widget = ImageWidget(self,event_flag=True)
        #self.layout = QtWidgets.QFormLayout(self.img_widget)
        self.img_widget.setGeometry(140,130,600,470)
        self.img_widget.setStyleSheet('border : 2px solid gray;')

        self.ctrl_widget = CtrlWindow(self)
        self.ctrl_widget.setGeometry(820,130,250,470)
        
        layout.addWidget(self.img_widget)
        layout.addWidget(self.ctrl_widget)

    #메뉴바 추가
    def add_menubar(self):
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Esc')#강제종료 키 esc
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        #상태바 추가
        self.add_statusbar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def closeEvent(self, event): #닫기 창 메시지박스 추가.
        quit_msg = "이미지 저장"
        reply = QMessageBox.question(self, '저장하시겠습니까?', quit_msg, QMessageBox.Yes, QMessageBox.No) #메시지박스

        if reply == QMessageBox.Yes:
            self.save_file()

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
        
        #rgb 평균값 할당.
        self.rgb = []
        a,b,c = cv2.split(self.img_original)
        self.rgb_2d_array =[c,b,a]

        mean_ch = cv2.mean(self.img)
        
        self.rgb.append(int(mean_ch[2]))
        self.rgb.append(int(mean_ch[1]))
        self.rgb.append(int(mean_ch[0]))
        
        self.update_img(self.img) #이미지 업데이트
        self.ctrl_widget.update_rgb_label(rb = self.rgb)

        if self.widget_cnt > 0:#도커 창 닫기
            dock.close()

    def save_img(self):
        if self.img_original is not None:
            print('어?')
            img_file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;")
            print(img_file_path)
            if img_file_path and self.img_original is not None:
                cv2.imwrite(img_file_path, self.img_original)
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

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass


    def focus_on(self):#이미지 프레임 포커싱 인  
        print('포커싱 인')
        self.focus_image_frame_flag = True
    def focus_off(self):#이미지 프레임 포커싱 아웃
        self.focus_image_frame_flag = False
        self.statusBar().clearMessage() #포커싱 아웃될때 메시지 제거 

    def savefile(self): #파일 저장하기 
        print('save file')     

    def update_statusBar(self,event):
        tracking_location  = "마우스 좌표 (x,y) = ({0}, {1}), global x,y = {2},{3}".format(event.x(),event.y(),event.globalX(),event.globalY())
        self.statusBar().showMessage(tracking_location)

    

############################################이미지 프로세싱#########################################################
    def update_img(self,img):
        self.img_widget.set_image(img)

    def update_r(self,dif):
        self.rgb[0] = cv2.add(self.rgb[0] , dif)#연산을 한다. 
        self.rgb_2d_array[0] = cv2.add(self.rgb_2d_array[0],dif)
        self.update_image_rgb()

    def update_g(self,dif):
        self.rgb[1] = cv2.add(self.rgb[1] , dif)
        self.rgb_2d_array[1] = cv2.add(self.rgb_2d_array[1],dif)
        self.update_image_rgb()

    def update_b(self,dif):
        self.rgb[2] = cv2.add(self.rgb[2] , dif)
        self.rgb_2d_array[2] = cv2.add(self.rgb_2d_array[2],dif)
        self.update_image_rgb()

    def update_image_rgb(self):
        im = cv2.merge(self.rgb_2d_array)
        self.update_img(im)
        
    #이미지 w, h 비율대로 resize 해서 왜곡을 피한다. 
    #코드 사용 예 image = image_resize(image, height = 800)
    def img_resize(image, width = None, height = None, inter = cv2.INTER_AREA):#inter area는 cv2제공하는 양선형 보간법이다. 
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
    
    #화이트 노이즈 뿌리는 함수
    def add_noise(img):
        global weight
        b,g,r = cv2.split(img)#rgb 분리
        rgb_list = [r,g,b]

        # img의 행 열을 가져온다.
        row , col = rgb_list[0].shape
        weight = int(math.sqrt(row * col // 40000)) #크기에 따른 노이즈 크기 조절
        if weight < 1 : weight =1 
        # 노이즈 개수 지정
        number_of_pixels = 10000*weight
        print(weight)
        for j in range(number_of_pixels):
            #랜덤 좌표에다 노이즈 부여 
            y=random.randint(0, row - 1-weight)
            x=random.randint(0, col - 1-weight)
            
            for i in range(3):#rgb 위치는 동일
                div_img = rgb_list[i] #rgb 리스트 하나 불러온 다음  
                #div_img[y:y+2][x:x+2] = 255 #(255,255,255) 가중치 네모 사이즈 만큼 흰색 노이즈 뿌린다.
                for a in range(weight):
                    for b in range(weight):
                        div_img[y+a][x+b] = 255
        
        img = cv2.merge(rgb_list) #rgb 합침
        return img
    
    #점묘법 필터 함수 
    def pointillism_filter(self,img):
        img_noise = self.add_noise(img.copy())
        kernel = np.ones((3*weight+1,3*weight+1), np.uint8) / 9 # 가중치에 따른 마스크 생성
        img_noise = cv2.erode(img_noise,kernel) #erode 연산으로 화이트 노이즈 없엠.
        return img_noise
    
    def get_rgb(self):
        return self.rgb
#############################################----------------#######################################################

############################################이미지 위젯 클래스#########################################################
class ImageWidget(QtWidgets.QWidget):
    event_flag = False # 콜백 함수 실행 여부 플래그
    focus = False # 마우스 포커싱 실행 여부 
    
    def __init__(self, parent=None,event_flag = False):
        super(ImageWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self.image_frame = QLabel(self) #이미지 프레임 생성
        self.image = np.zeros((3,3),np.uint8)
        self.image_frame.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)
        if parent is not None:
            self.set_image(parent.img_original)
        self.event_flag = event_flag #이벤트 플래그 설정
        self.parent = parent

    def set_image(self,img): #이미지 변경
        self.image = img
        self.show_image()
        
    def d_mouseMoveEvent(self, event):#마우스 움직임 이벤트  
        if self.event_flag:
            print('자식')
            self.parent.update_statusBar(event)

    @pyqtSlot()
    def show_image(self): # Qimage 객체가 필요하다. 
        self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))
    
    def enterEvent(self, event): #들어온다.
        if self.event_flag :
            self.parent.focus_on()
            self.focus = True
            print('hover')
    #todo 들어오면 마우스 감지, 화면에 이미지 띄우는 스레드 실행 하기
    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def mouseMoveEvent(self, event):#마우스 움직임 이벤트 
        print('마우스 움직임')
       #self.img_widget.my_onMouse(event)
        self.parent.update_statusBar(event)

    def leaveEvent(self, event): #마우스 포커싱 나갈때
        if self.event_flag :
            self.parent.focus_off()
            self.focus = False
            print('left')

    def get_focus(self):
        return self.focus



############################################--------------#########################################################

if __name__ == '__main__': #실행이 main함수인 경우
    app = QApplication(sys.argv)
    ex = Photoshop()
    sys.exit(app.exec_())
