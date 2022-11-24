import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
import os

class MyApp(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.initUI()
        
    def initUI(self):    
        
        self.setGeometry(200, 200, 200, 200)           
        
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Esc') #단축키 추가 메소드
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.setWindowTitle('PyQt5 Basic Menubar')    
        self.show()

    #버튼 추가
    def add_btn(self):
        img_path_btn = QPushButton('불러오기', self)
        img_path_btn.resize(img_path_btn.sizeHint())
        img_path_btn.setToolTip('이미지를 불러옵니다')
        img_path_btn.clicked.connect(QCoreApplication.instance().quit) #버튼 이벤트 처리 
        img_path_btn.move(50, 50) #위치이동
    
    #메뉴바 추가
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
        
if __name__ == '__main__': #실행이 main함수인 경우
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
