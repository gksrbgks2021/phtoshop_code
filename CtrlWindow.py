#!/usr/bin/python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QSlider, QSpinBox, \
    QGridLayout, QTextEdit, QDoubleSpinBox

class CtrlWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.rgb = [128,128,128]

        self.init_ui()

    def init_ui(self):#ui 초기화 ~ 
        self.rootVbox = QVBoxLayout()
        self.tab1 = QWidget()
        self.tab1.setObjectName('parent')
        self.tab1.setStyleSheet('QWidget#parent{border : 2px solid gray;}')#부모 에게만 경계선 지정하기.

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
        self.r_level.setValue(self.rgb[0])
        self.tab1.layout.addWidget(self.r_level)
        self.r_level.valueChanged.connect(self.change_r)#이벤트

        self.g_level_label = QLabel("초 록 : 127")
        self.tab1.layout.addWidget(self.g_level_label)
        self.g_level = QSlider(Qt.Horizontal)
        self.g_level.setTickPosition(QSlider.TicksBelow)
        self.g_level.setTickInterval(64)
        self.g_level.setMinimum(0)# 0 .. 255 
        self.g_level.setMaximum(255)
        self.g_level.setValue(self.rgb[1])
        self.tab1.layout.addWidget(self.g_level)
        self.g_level.valueChanged.connect(self.change_g)

        self.b_level_label = QLabel("파 랑: 127")
        self.tab1.layout.addWidget(self.b_level_label)
        self.b_level = QSlider(Qt.Horizontal)
        self.b_level.setTickPosition(QSlider.TicksBelow)
        self.b_level.setTickInterval(64)
        self.b_level.setMinimum(0)# 0 .. 255 
        self.b_level.setMaximum(255)
        self.b_level.setValue(self.rgb[2])
        self.tab1.layout.addWidget(self.b_level)
        self.b_level.valueChanged.connect(self.change_b)

        btn14 = QPushButton('RGB')
        btn14.setIcon(QIcon('Icons/rgb.png'))
        #btn14.clicked.connect(self.parent.handler.handle_rgb)
        self.tab1.layout.addWidget(btn14)

        btn7 = QPushButton('Threshold')
        btn7.setIcon(QIcon('Icons/threshold.png'))
       # btn7.clicked.connect(self.parent.handler.handle_threshold)
        self.tab1.layout.addWidget(btn7)

    def change_r(self):
        dif = self.r_level.value() - self.rgb[0] #차이 만큼 변화 시킨다.
        self.rgb[0] = self.r_level.value()#슬라이더의 빨간 값을 가져온다.
        self.parent.update_r(dif)
        self.update_rgb_label()

    def change_g(self):
        dif = self.r_level.value() - self.rgb[1]
        self.rgb[1] = self.g_level.value()#슬라이더의 초록 값을 가져온다. 
        self.parent.update_g(dif)
        self.update_rgb_label()

    def change_b(self):
        dif = self.r_level.value() - self.rgb[2]
        self.rgb[2] = self.b_level.value()#슬라이더의 파랑 값을 가져온다. 
        self.parent.update_b(dif)
        self.update_rgb_label()
    
    def update_rgb_label(self,rb = None):
        if rb:
            self.rgb = rb

        self.r_level_label.setText("빨 강 : " + str(self.rgb[0]))
        self.g_level_label.setText("초 록 : " + str(self.rgb[1]))
        self.b_level_label.setText("파 랑 : " + str(self.rgb[2]))