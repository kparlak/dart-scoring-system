# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_game_display.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectGameDisplay(object):
    def setupUi(self, SelectGameDisplay):
        SelectGameDisplay.setObjectName("SelectGameDisplay")
        SelectGameDisplay.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(SelectGameDisplay)
        self.centralwidget.setObjectName("centralwidget")
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(10, 370, 75, 25))
        self.helpButton.setObjectName("helpButton")
        self.selectPlayersButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectPlayersButton.setGeometry(QtCore.QRect(300, 220, 200, 100))
        self.selectPlayersButton.setObjectName("selectPlayersButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(715, 370, 75, 25))
        self.cancelButton.setObjectName("cancelButton")
        self.gameLabel = QtWidgets.QLabel(self.centralwidget)
        self.gameLabel.setGeometry(QtCore.QRect(180, 100, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.gameLabel.setFont(font)
        self.gameLabel.setObjectName("gameLabel")
        self.gameBox = QtWidgets.QComboBox(self.centralwidget)
        self.gameBox.setGeometry(QtCore.QRect(280, 100, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.gameBox.setFont(font)
        self.gameBox.setObjectName("gameBox")
        self.gameBox.addItem("")
        self.gameBox.addItem("")
        SelectGameDisplay.setCentralWidget(self.centralwidget)

        self.retranslateUi(SelectGameDisplay)
        QtCore.QMetaObject.connectSlotsByName(SelectGameDisplay)

    def retranslateUi(self, SelectGameDisplay):
        _translate = QtCore.QCoreApplication.translate
        SelectGameDisplay.setWindowTitle(_translate("SelectGameDisplay", "Select Game"))
        self.helpButton.setText(_translate("SelectGameDisplay", "Help"))
        self.selectPlayersButton.setText(_translate("SelectGameDisplay", "Select Players"))
        self.cancelButton.setText(_translate("SelectGameDisplay", "Cancel"))
        self.gameLabel.setText(_translate("SelectGameDisplay", "Select Game"))
        self.gameBox.setItemText(0, _translate("SelectGameDisplay", "501"))
        self.gameBox.setItemText(1, _translate("SelectGameDisplay", "Around the World"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SelectGameDisplay = QtWidgets.QMainWindow()
    ui = Ui_SelectGameDisplay()
    ui.setupUi(SelectGameDisplay)
    SelectGameDisplay.show()
    sys.exit(app.exec_())
