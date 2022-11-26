import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
import numpy as np, cv2
import matplotlib.pyplot as plt
import os

class MyApp(QMainWindow):
    #전역변수 설정
    img_original  = np.zeros((3,3),np.uint8)
    img  = np.zeros((3,3),np.uint8)
    img_list = []
    widget_cnt = 0
    focus_image_frame_flag = False #자식 마우스 이벤트 플래그
    
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
        self.add_widget()
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
    
    def add_widget(self): # 위젯 추가
        self.img_widget = ImageWidget(self,event_flag=True)
        #self.layout = QtWidgets.QFormLayout(self.img_widget)
        self.img_widget.setGeometry(140,130,600,470)
        self.img_widget.setStyleSheet('border : 2px solid gray;')

        self.ctrl_widget = ctrl_Widget(self)
        self.ctrl_widget.setStyleSheet('background: red;')
        
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
        
        self.update_img(self.img) #이미지 업데이트
        
        if self.widget_cnt > 0:#도커 창 닫기
            dock.close()

    def save_img(self):
        if self.img_original is not None:
            img_file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;")

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
        self.img_widget.show()

    #이미지 원래 비율대로 맞추서ㅓ 사이즈 조정한다. 
    def img_resize(image, width = None, height = None, inter = cv2.INTER_AREA):#inter area는 cv2제공하는 양선형 보간법이다. 
        if width is None and height is None:#widght, height 값이 없으면 
            return image
        # 이미지 widght, height
        dim = None
        (h, w) = image.shape[:2]

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        #크기 재조정. 
        resized = cv2.resize(image, dim, interpolation = inter)
        return resized
####################################################################################################################

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

############################################컨트롤 위젯 클래스#########################################################
class ctrl_Widget(QtWidgets.QWidget):
#size 280 x 670 
    def __init__(self, parent=None):        
        super(ctrl_Widget, self).__init__(parent) # mainwindow 안에 위젯 추가
        self.initUI()

    def initUI(self):
        label1 = QLabel('First Label', self)
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel('Second Label', self)
        label2.setAlignment(Qt.AlignVCenter)

        font1 = label1.font()
        font1.setPointSize(20)

        font2 = label2.font()
        font2.setFamily('Times New Roman')
        font2.setBold(True)

        label1.setFont(font1)
        label2.setFont(font2)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)

        self.setLayout(layout)
        self.setGeometry(850, 132, 300,600 )

    def add_label(self):
        self.label_trackbar_r = QLabel('Red', self)
        self.label_trackbar_g = QLabel('Green', self)
        self.label_trackbar_b = QLabel('Blue', self)
        self.label_trackbar_h = QLabel('Hue', self)
        self.label_trackbar_s = QLabel('Saturation', self)
        self.label_trackbar_v = QLabel('Value', self)
    
    
        

    

############################################--------------#########################################################
if __name__ == '__main__': #실행이 main함수인 경우
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
