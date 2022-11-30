#!/usr/bin/python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QPushButton

#컨트롤바 윈도우 
class YesOrNo(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.init_ui()

    def init_ui(self):#ui 초기화 ~ 
        self.rootVbox = QVBoxLayout()
        self.tab1 = QWidget()
        self.tab1.setObjectName('yon')
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
        btn_ok = QPushButton('확 인')
        btn_ok.setIcon(QIcon('img/ok.png'))
        btn_ok.clicked.connect(self.parent.click_ok)
        self.tab1.layout.addWidget(btn_ok)

        btn_no = QPushButton('취 소')
        btn_no.setIcon(QIcon('img/cancle.png'))
        btn_no.clicked.connect(self.parent.click_cancle)
        self.tab1.layout.addWidget(btn_no)