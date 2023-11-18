# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_profile_display.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateProfileDisplay(object):
    def setupUi(self, CreateProfileDisplay):
        CreateProfileDisplay.setObjectName("CreateProfileDisplay")
        CreateProfileDisplay.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(CreateProfileDisplay)
        self.centralwidget.setObjectName("centralwidget")
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(10, 370, 75, 25))
        self.helpButton.setObjectName("helpButton")
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(300, 220, 200, 100))
        self.uploadButton.setObjectName("uploadButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(715, 370, 75, 25))
        self.cancelButton.setObjectName("cancelButton")
        self.nameInput = QtWidgets.QTextEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(280, 100, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nameInput.setFont(font)
        self.nameInput.setObjectName("nameInput")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(180, 100, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setGeometry(QtCore.QRect(180, 140, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.usernameInput = QtWidgets.QTextEdit(self.centralwidget)
        self.usernameInput.setGeometry(QtCore.QRect(280, 140, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameInput.setFont(font)
        self.usernameInput.setObjectName("usernameInput")
        CreateProfileDisplay.setCentralWidget(self.centralwidget)

        self.retranslateUi(CreateProfileDisplay)
        QtCore.QMetaObject.connectSlotsByName(CreateProfileDisplay)

    def retranslateUi(self, CreateProfileDisplay):
        _translate = QtCore.QCoreApplication.translate
        CreateProfileDisplay.setWindowTitle(_translate("CreateProfileDisplay", "Create Profile"))
        self.helpButton.setText(_translate("CreateProfileDisplay", "Help"))
        self.uploadButton.setText(_translate("CreateProfileDisplay", "Upload"))
        self.cancelButton.setText(_translate("CreateProfileDisplay", "Cancel"))
        self.nameLabel.setText(_translate("CreateProfileDisplay", "Name"))
        self.usernameLabel.setText(_translate("CreateProfileDisplay", "Username"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProfileDisplay = QtWidgets.QMainWindow()
    ui = Ui_CreateProfileDisplay()
    ui.setupUi(CreateProfileDisplay)
    CreateProfileDisplay.show()
    sys.exit(app.exec_())
