# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\cmp.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1118, 864)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 3, 1, 1, 1)
        self.gridLayout_0 = QtWidgets.QGridLayout()
        self.gridLayout_0.setObjectName("gridLayout_0")
        self.lineEdit_0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_0.setObjectName("lineEdit_0")
        self.gridLayout_0.addWidget(self.lineEdit_0, 1, 0, 1, 1)
        self.pushButton_0 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_0.setObjectName("pushButton_0")
        self.gridLayout_0.addWidget(self.pushButton_0, 4, 0, 1, 1)
        self.toolButton_0 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_0.setObjectName("toolButton_0")
        self.gridLayout_0.addWidget(self.toolButton_0, 1, 1, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout_0.addWidget(self.pushButton_1, 6, 0, 1, 1)
        self.toolButton_1 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_1.setObjectName("toolButton_1")
        self.gridLayout_0.addWidget(self.toolButton_1, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_0.addItem(spacerItem, 8, 0, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.gridLayout_0.addWidget(self.label_1, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_0.addItem(spacerItem1, 9, 0, 1, 1)
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setObjectName("label_0")
        self.gridLayout_0.addWidget(self.label_0, 0, 0, 1, 1)
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.gridLayout_0.addWidget(self.lineEdit_1, 3, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_0.addWidget(self.textEdit, 7, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_0, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_0.setText(_translate("MainWindow", "PushButton"))
        self.toolButton_0.setText(_translate("MainWindow", "..."))
        self.pushButton_1.setText(_translate("MainWindow", "PushButton"))
        self.toolButton_1.setText(_translate("MainWindow", "..."))
        self.label_1.setText(_translate("MainWindow", "TextLabel"))
        self.label_0.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

