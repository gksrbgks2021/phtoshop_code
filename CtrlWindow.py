#!/usr/bin/python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QSlider, QSpinBox, \
    QGridLayout, QTextEdit, QDoubleSpinBox
import numpy as np, cv2

#컨트롤바 윈도우 
class CtrlWindow(QFrame):
 
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent
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

        btn_flip = QPushButton('R G B')
        btn_flip.clicked.connect(self.parent.rgbtrack)
        self.tab1.layout.addWidget(btn_flip)

        btn_flip = QPushButton('좌우반전')
        btn_flip.clicked.connect(self.parent.flip)
        self.tab1.layout.addWidget(btn_flip)

        btn_rotate_90 = QPushButton('90도 회전')
        btn_rotate_90.clicked.connect(self.parent.rotate)
        self.tab1.layout.addWidget(btn_rotate_90)

        btn_filter_1 = QPushButton('점묘법 필터1')
        btn_filter_1.setIcon(QIcon('Icons/rgb.png'))
        btn_filter_1.clicked.connect(self.parent.filter_1)
        self.tab1.layout.addWidget(btn_filter_1)
        
        btn_filter_2 = QPushButton('점묘법 필터2')
        btn_filter_2.setIcon(QIcon('Icons/rgb.png'))
        btn_filter_2.clicked.connect(self.parent.filter_2)
        self.tab1.layout.addWidget(btn_filter_2)

        btn_filter_3 = QPushButton('반전 필터')#todo
        btn_filter_3.setIcon(QIcon('Icons/rgb.png'))
        btn_filter_3.clicked.connect(self.parent.filter_2)
        self.tab1.layout.addWidget(btn_filter_3)

        btn_clip = QPushButton('잘라내기')#todo
        btn_clip.clicked.connect(self.parent.filter_2)
        self.tab1.layout.addWidget(btn_clip)

        btn_resize = QPushButton('화면 맞추기')#todo
        btn_resize.clicked.connect(self.parent.filter_2)
        self.tab1.layout.addWidget(btn_resize)