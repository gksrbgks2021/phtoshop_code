#!/usr/bin/python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np, cv2

#컨트롤바 윈도우 
class RgbFrame(QFrame):
    flag = True

    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.rgb = np.zeros((3,3,3))
        self.rgb_mean = [128,128,128]

        self.init_ui()

    def init_ui(self):#ui 초기화 ~ 
        self.rootVbox = QVBoxLayout()
        self.tab1 = QWidget()
        self.tab1.setObjectName('rgb')
        self.tab1.setStyleSheet('QWidget#parent{border : 2px solid gray;')#부모 에게만 경계선 지정하기.
        
        #탭 추가
        self.init_tab1()

        self.rootVbox.addWidget(self.tab1)
        self.setLayout(self.rootVbox)

    def init_tab1(self):
        self.tab1.layout = QVBoxLayout(self) # 수직 레이아웃설정
        self.tab1.layout.setAlignment(Qt.AlignTop)#위로 정렬
        self.tab1.layout.setSpacing(12)
        self.init_rgb_slider() #rgb 슬라이더 추가 
        self.tab1.setLayout(self.tab1.layout)

        self.tab1.layout.addWidget(QLabel(" "))

    def init_rgb_slider(self): #rgb 슬라이더 바 만듭니다.
        self.r_level_label = QLabel("빨 강 : 127")
        self.tab1.layout.addWidget(self.r_level_label)
        self.r_level = QSlider(Qt.Horizontal)
        self.r_level.setTickPosition(QSlider.TicksBelow)
        self.r_level.setTickInterval(64)#간격 설정
        self.r_level.setMinimum(0)# 0 .. 255 
        self.r_level.setMaximum(255)
        self.r_level.setValue(127)
        self.tab1.layout.addWidget(self.r_level)

        self.g_level_label = QLabel("초 록 : 127")
        self.tab1.layout.addWidget(self.g_level_label)
        self.g_level = QSlider(Qt.Horizontal)
        self.g_level.setTickPosition(QSlider.TicksBelow)
        self.g_level.setTickInterval(64)
        self.g_level.setMinimum(0)# 0 .. 255 
        self.g_level.setMaximum(255)
        self.g_level.setValue(127)
        self.tab1.layout.addWidget(self.g_level)
        
        self.b_level_label = QLabel("파 랑: 127")
        self.tab1.layout.addWidget(self.b_level_label)
        self.b_level = QSlider(Qt.Horizontal)
        self.b_level.setTickPosition(QSlider.TicksBelow)
        self.b_level.setTickInterval(64)
        self.b_level.setMinimum(0)# 0 .. 255 
        self.b_level.setMaximum(255)
        self.b_level.setValue(127)
        self.tab1.layout.addWidget(self.b_level)

        btn_ok = QPushButton('')
        btn_ok.setIcon(QIcon('./img/ok.png'))
        btn_ok.setIconSize(QSize(30,30))
        btn_ok.clicked.connect(self.parent.click_ok)

        self.tab1.layout.addWidget(btn_ok)

        btn_no = QPushButton('')
        btn_no.setIcon(QIcon('./img/cancle.png'))
        btn_no.setIconSize(QSize(30,30))
        btn_no.clicked.connect(self.parent.click_cancle)
        self.tab1.layout.addWidget(btn_no)

####################################프레임 불러오고 트리거 메소드###############################################

    #이미지 불러올때 트랙바 초기화
    def init_track(self, Prgb):
        #rgb 트랙바 초기화 
        self.rgb_mean[0] = Prgb[0]
        self.r_level.setValue(self.rgb_mean[0])
        self.r_level.valueChanged.connect(self.change_r)#이벤트

        self.rgb_mean[1] = Prgb[1]
        self.g_level.setValue(self.rgb_mean[1])
        self.g_level.valueChanged.connect(self.change_g)

        self.rgb_mean[2] = Prgb[2]
        self.b_level.setValue(self.rgb_mean[2])
        self.b_level.valueChanged.connect(self.change_b)
        self.r_level_label.setText("빨 강 : " + str(self.rgb_mean[0]))
        self.r_level_label.setText("빨 강 : " + str(self.rgb_mean[1]))
        self.g_level_label.setText("초 록 : " + str(self.rgb_mean[2]))
        
        self.flag = False #트랙바 이벤트 활성화 !!

    def change_r(self):
        self.r_level_label.setText("빨 강 : " + str(self.r_level.value()))

        if self.flag : return #트랙바가 꺼져있으면 작동 x, 그래야 다음 트랙바 불러올때 작동안함. 
        dif = self.r_level.value() - self.rgb_mean[0] #차이 만큼 변화 시킨다.
        self.parent.change_img_rgb(dif,0)#부모에게 차이를 넘겨준다
    
        

    def change_g(self):
        self.g_level_label.setText("초 록 : " + str(self.g_level.value()))
        if self.flag : return #트랙바가 꺼져있으면 작동 x, 그래야 다음 트랙바 불러올때 작동안함. 
        dif = self.g_level.value() - self.rgb_mean[1]
        self.parent.change_img_rgb(dif,1)
        

    def change_b(self):
        self.b_level_label.setText("파 랑 : " + str(self.b_level.value()))
        if self.flag : return #트랙바가 꺼져있으면 작동 x, 그래야 다음 트랙바 불러올때 작동안함. 
        dif = self.b_level.value() - self.rgb_mean[2]
        
        self.parent.change_img_rgb(dif,2)
        

    def close_trackbar(self):
        self.flag = True
    
####################################-----------------------###############################################

    def display_img_af(self,dif,rgb_flag):#이미지 차이를 부모에게 넘겨준다.  
        rgb = self.parent.get_rgb()

        if rgb_flag == 0:#Red
            r = self.parent.get_r()
            self.rgb[0] = cv2.add(r, dif)#연산을 한다. 
        elif rgb_flag ==1:#Green
            g = self.parent.get_g()
            self.rgb[1] = cv2.add(g , dif)
        elif rgb_flag ==2:#Blue
            b = self.parent.get_b()
            self.rgb[2] = cv2.add(b, dif)

        self.update_rgb_label()
        
    def update_rgb_label(self,rb = None):# 클릭 버튼을 눌러 이미지를 바꿉니다.
        if rb:#이미지 바꿨을때.
            self.rgb = rb
            self.parent.update_rgb(self.rgb) 

            btn_clip = QPushButton('잘라내기')#todo
        btn_clip.clicked.connect(self.parent.filter_2)
        self.tab1.layout.addWidget(btn_clip)