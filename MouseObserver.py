from PyQt5.QtCore import (
    pyqtSignal,
    QEvent,
    QObject,
    QPoint,
    Qt,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

class MouseObserver(QObject):
    pressed = pyqtSignal(QPoint, QPoint)
    released = pyqtSignal(QPoint, QPoint)
    moved = pyqtSignal(QPoint, QPoint)
    
    def __init__(self, window):
        super().__init__(window)
        self._window = window
        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window
        
    def registerSignal(self, obj):
        self.pressed.connect(obj)
        self.released.connect(obj)
        self.moved.connect(obj)
    
    def eventFilter(self, obj, event):#이벤트 처리 필터를 만든다.
        if self.window is obj:
            if event.type() == QEvent.MouseButtonPress:
                self.pressed.emit(event.pos(), event.globalPos())
            elif event.type() == QEvent.MouseMove:
                #obj.my_moveEvent(event)
                self.moved.emit(event.pos(), event.globalPos())
                return super(MouseObserver, self).eventFilter(obj, event)

            elif event.type() == QEvent.MouseButtonRelease:
                self.released.emit(event.pos(), event.globalPos())
        return super().eventFilter(obj, event)

