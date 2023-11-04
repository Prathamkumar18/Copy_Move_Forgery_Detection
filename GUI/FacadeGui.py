import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore
from Detector.SiftDetector import SiftDetector


class Facade():
    size = 720
    NPundo = np.empty((2, 2))
    NPimg = np.empty((2, 2))

    def setupUi(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(720, 720)
        main_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        main_window.setMouseTracking(False)
        main_window.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                  "selection-background-color: rgb(135, 171, 255);\n"
                                  "background-color: rgb(255, 255, 255);\n")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setStyleSheet("QLabel{ background-color : rgb(204, 231, 232); color : black; }")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        main_window.setCentralWidget(self.centralwidget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(1, 5, 636, 21))
        self.menu_bar.setObjectName("menubar")
        self.q_menu = QtWidgets.QMenu(self.menu_bar)
        self.q_menu.setObjectName("menuMenu")
        main_window.setMenuBar(self.menu_bar)
        self.tool_bar = QtWidgets.QToolBar(main_window)
        self.tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.tool_bar.setObjectName("toolBar")
        main_window.addToolBar(QtCore.Qt.LeftToolBarArea, self.tool_bar)
        self.action_Open = QtWidgets.QAction(main_window)
        self.action_Open.setObjectName("actionOpen")
        self.action_Undo = QtWidgets.QAction(main_window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Undo.setIcon(icon)
        self.action_Undo.setObjectName("actionUndo")

        icon2 = QtGui.QIcon()
        self.action_Sift = QtWidgets.QAction(main_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/sift.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Sift.setIcon(icon3)
        self.action_Sift.setObjectName("actionSift")



        self.q_menu.addAction(self.action_Open)
        self.menu_bar.addAction(self.q_menu.menuAction())
        self.tool_bar.addAction(self.action_Undo)
        self.tool_bar.addAction(self.action_Sift)
        self.translateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def translateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "CMDF"))
        self.q_menu.setTitle(_translate("MainWindow", "Menu"))
        self.tool_bar.setWindowTitle(_translate("MainWindow", "Operations"))
        self.action_Open.setText(_translate("MainWindow", "Choose Image"))
        self.action_Undo.setText(_translate("MainWindow", "Reset"))
        self.action_Undo.setToolTip(_translate("MainWindow", "Undo"))
        self.action_Sift.setText(_translate("MainWindow", "SIFT"))
        self.action_Sift.setToolTip(_translate("MainWindow", "Sift-Based Detection"))
        self.action_Open.triggered.connect(self.openImage)
        self.action_Sift.triggered.connect(self.siftDetector)
        self.action_Undo.triggered.connect(self.undo)

    @staticmethod
    def undo(self):
        self.image = self.origImage.copy()
        self.showImage(self.image)

    def backup(self):
        self.NPundo = self.NPimg

    def openImage(self):
        self.backup()
        root = tk.Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(initialdir="~",
                                                   title="Select File",
                                                   filetypes=(("jpeg files", "*.jpeg"), ("all files", "*.*")))
        if root.filename:
            # img = Image.open(root.filename)
            self.image = cv2.imread(root.filename, cv2.IMREAD_COLOR)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.origImage = self.image.copy()
            self.showImage(self.origImage)

    def showImage(self, img_show):
        image_profile = QtGui.QImage(img_show, img_show.shape[1], img_show.shape[0], img_show.shape[1] * 3,
                                     QtGui.QImage.Format_RGB888)  # QImage object
        image_profile = image_profile.scaled(self.size, self.size, aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image_profile))

    def siftDetector(self):
        sift = SiftDetector(self.image)
        self.image = sift.image
        self.showImage(self.image)