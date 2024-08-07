from PyQt5 import QtCore, QtGui, QtWidgets
import base64
from gambar import *
from PyQt5.QtCore import Qt

class ProgressBarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.baca_icon = QtGui.QPixmap()
        self.baca_icon.loadFromData(base64.b64decode(Gambar_Icon_App))  
        self.setWindowIcon(QtGui.QIcon(self.baca_icon))
        self.setWindowTitle("Kemajuan Encoding | Copyright (c) 2023 by Arif Maulana")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(100, 100, 470, 45)

        self.title_bar_visible = True  # Flag to track the title bar visibility

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.progressBar = QtWidgets.QProgressBar(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progressBar.setFont(font)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)

        self.eventFilter = EventFilter(self.progressBar)
        self.progressBar.installEventFilter(self.eventFilter)

        self.updateProgressBarStyle()

        self.draggable = False
        self.offset = None

    def setPercentage(self, percentage, text=None):
        self.progressBar.setValue(percentage)
        if text is not None:
            self.progressBar.setFormat(text)

    def updateProgressBarStyle(self):
        self.progressBar.setStyleSheet("""
            QProgressBar {
                color: black;
            }
        """)

    def mouseDoubleClickEvent(self, event):
        if event.pos().x() >= self.progressBar.geometry().x() and event.pos().x() <= self.progressBar.geometry().x() + self.progressBar.geometry().width() \
           and event.pos().y() >= self.progressBar.geometry().y() and event.pos().y() <= self.progressBar.geometry().y() + self.progressBar.geometry().height():
            self.toggle_title_bar()

    def toggle_title_bar(self):
        if self.title_bar_visible:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.draggable = True
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.draggable = False
        self.show()
        self.title_bar_visible = not self.title_bar_visible

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = None

class EventFilter(QtCore.QObject):
    def __init__(self, progressBar):
        super().__init__()
        self.progressBar = progressBar

    def eventFilter(self, obj, event):
        if obj == self.progressBar and event.type() == QtCore.QEvent.Resize:
            self.updateProgressBarFontSize()
        return super().eventFilter(obj, event)
        
    def updateProgressBarFontSize(self):
        font = self.progressBar.font()
        font.setPointSizeF(min(self.progressBar.height() * 0.5, 80))
        self.progressBar.setFont(font)

