import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
import os

#이미지 불러올때 화면 크기에 맞춰서 불러오기 (ex : 300x300 으로 했으면 이미지  축소, )
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI() #초기화..
        
    def initUI(self):
        self.title = '포토샵 구현' #제목
        self.setWindowIcon(QIcon('./img/cat.jpg'))
        self.left = 15
        self.top = 40
        self.width = 1900
        self.height = 950
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) #크기 세팅
        
        self.add_btn() #버튼추가..
        #self.add_menubar() #메뉴바 추가

        self.show() #화면에 띄운다.
        
    def add_btn(self):
        img_path_btn = QPushButton('불러오기', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('이미지를 불러옵니다')
        img_path_btn.clicked.connect(QCoreApplication.instance().quit) #버튼 이벤트 처리 
        img_path_btn.move(50, 50) #위치이동
    
    def add_menubar(self):
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def closeEvent(self, event): #닫기 창 메시지박스 추가.
        quit_msg = "이미지 저장"
        reply = QMessageBox.question(self, '저장하시겠습니까?', quit_msg, QMessageBox.Yes, QMessageBox.No) #메시지박스

        if reply == QMessageBox.Yes:
            self.save_file()

        event.accept()

    def save_file(self):
        print('저장완료')
        
    
if __name__ == '__main__': #main함수 실행. 
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) #프로그램 종료를 한다. 