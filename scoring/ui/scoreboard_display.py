# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scoreboard_display.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScoreboardDisplay(object):
    def setupUi(self, ScoreboardDisplay):
        ScoreboardDisplay.setObjectName("ScoreboardDisplay")
        ScoreboardDisplay.resize(800, 400)
        ScoreboardDisplay.setWindowTitle("")
        self.centralwidget = QtWidgets.QWidget(ScoreboardDisplay)
        self.centralwidget.setObjectName("centralwidget")
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(10, 370, 75, 25))
        self.helpButton.setObjectName("helpButton")
        self.player1Button = QtWidgets.QPushButton(self.centralwidget)
        self.player1Button.setGeometry(QtCore.QRect(20, 160, 200, 100))
        self.player1Button.setObjectName("player1Button")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(715, 370, 75, 25))
        self.quitButton.setObjectName("quitButton")
        self.player2Button = QtWidgets.QPushButton(self.centralwidget)
        self.player2Button.setGeometry(QtCore.QRect(580, 160, 200, 100))
        self.player2Button.setObjectName("player2Button")
        self.player1Label = QtWidgets.QLabel(self.centralwidget)
        self.player1Label.setGeometry(QtCore.QRect(80, 50, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.player1Label.setFont(font)
        self.player1Label.setAlignment(QtCore.Qt.AlignCenter)
        self.player1Label.setObjectName("player1Label")
        self.player1UsernameOutput = QtWidgets.QTextEdit(self.centralwidget)
        self.player1UsernameOutput.setGeometry(QtCore.QRect(40, 90, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.player1UsernameOutput.setFont(font)
        self.player1UsernameOutput.setReadOnly(True)
        self.player1UsernameOutput.setObjectName("player1UsernameOutput")
        self.player2ScoreOutput = QtWidgets.QTextEdit(self.centralwidget)
        self.player2ScoreOutput.setGeometry(QtCore.QRect(630, 280, 100, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.player2ScoreOutput.setFont(font)
        self.player2ScoreOutput.setReadOnly(True)
        self.player2ScoreOutput.setObjectName("player2ScoreOutput")
        self.player2Label = QtWidgets.QLabel(self.centralwidget)
        self.player2Label.setGeometry(QtCore.QRect(640, 50, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.player2Label.setFont(font)
        self.player2Label.setAlignment(QtCore.Qt.AlignCenter)
        self.player2Label.setObjectName("player2Label")
        self.player2UsernameOutput = QtWidgets.QTextEdit(self.centralwidget)
        self.player2UsernameOutput.setGeometry(QtCore.QRect(600, 90, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.player2UsernameOutput.setFont(font)
        self.player2UsernameOutput.setReadOnly(True)
        self.player2UsernameOutput.setObjectName("player2UsernameOutput")
        self.player1Score = QtWidgets.QLCDNumber(self.centralwidget)
        self.player1Score.setGeometry(QtCore.QRect(70, 280, 100, 50))
        self.player1Score.setSmallDecimalPoint(False)
        self.player1Score.setDigitCount(3)
        self.player1Score.setObjectName("player1Score")
        ScoreboardDisplay.setCentralWidget(self.centralwidget)

        self.retranslateUi(ScoreboardDisplay)
        QtCore.QMetaObject.connectSlotsByName(ScoreboardDisplay)

    def retranslateUi(self, ScoreboardDisplay):
        _translate = QtCore.QCoreApplication.translate
        self.helpButton.setText(_translate("ScoreboardDisplay", "Help"))
        self.player1Button.setText(_translate("ScoreboardDisplay", "Player 1"))
        self.quitButton.setText(_translate("ScoreboardDisplay", "Quit"))
        self.player2Button.setText(_translate("ScoreboardDisplay", "Player 2"))
        self.player1Label.setText(_translate("ScoreboardDisplay", "Player:"))
        self.player2Label.setText(_translate("ScoreboardDisplay", "Player:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ScoreboardDisplay = QtWidgets.QMainWindow()
    ui = Ui_ScoreboardDisplay()
    ui.setupUi(ScoreboardDisplay)
    ScoreboardDisplay.show()
    sys.exit(app.exec_())