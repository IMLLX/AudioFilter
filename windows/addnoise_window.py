# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addnoise_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddNoise(object):
    def setupUi(self, AddNoise):
        AddNoise.setObjectName("AddNoise")
        AddNoise.resize(491, 528)
        self.SNR_Level = QtWidgets.QLabel(AddNoise)
        self.SNR_Level.setGeometry(QtCore.QRect(20, 170, 72, 15))
        self.SNR_Level.setObjectName("SNR_Level")
        self.SNR_Level_text = QtWidgets.QTextBrowser(AddNoise)
        self.SNR_Level_text.setGeometry(QtCore.QRect(20, 190, 191, 41))
        self.SNR_Level_text.setReadOnly(False)
        self.SNR_Level_text.setObjectName("SNR_Level_text")
        self.verticalLayoutWidget = QtWidgets.QWidget(AddNoise)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 270, 431, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.apply_button = QtWidgets.QPushButton(AddNoise)
        self.apply_button.setGeometry(QtCore.QRect(360, 80, 93, 28))
        self.apply_button.setObjectName("apply_button")
        self.confirm_button = QtWidgets.QPushButton(AddNoise)
        self.confirm_button.setGeometry(QtCore.QRect(360, 120, 93, 28))
        self.confirm_button.setObjectName("confirm_button")
        self.cancel_button = QtWidgets.QPushButton(AddNoise)
        self.cancel_button.setGeometry(QtCore.QRect(360, 160, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.noise_method = QtWidgets.QLabel(AddNoise)
        self.noise_method.setGeometry(QtCore.QRect(20, 30, 72, 15))
        self.noise_method.setObjectName("noise_method")
        self.method_combo = QtWidgets.QComboBox(AddNoise)
        self.method_combo.setGeometry(QtCore.QRect(20, 50, 191, 41))
        self.method_combo.setObjectName("method_combo")
        self.sample_rate_text = QtWidgets.QTextBrowser(AddNoise)
        self.sample_rate_text.setGeometry(QtCore.QRect(20, 120, 191, 41))
        self.sample_rate_text.setReadOnly(False)
        self.sample_rate_text.setObjectName("sample_rate_text")
        self.sample_rate_label = QtWidgets.QLabel(AddNoise)
        self.sample_rate_label.setGeometry(QtCore.QRect(20, 100, 91, 16))
        self.sample_rate_label.setObjectName("sample_rate_label")

        self.retranslateUi(AddNoise)
        QtCore.QMetaObject.connectSlotsByName(AddNoise)

    def retranslateUi(self, AddNoise):
        _translate = QtCore.QCoreApplication.translate
        AddNoise.setWindowTitle(_translate("AddNoise", "Add Noise"))
        self.SNR_Level.setText(_translate("AddNoise", "SNR_Level"))
        self.apply_button.setText(_translate("AddNoise", "apply"))
        self.confirm_button.setText(_translate("AddNoise", "confirm"))
        self.cancel_button.setText(_translate("AddNoise", "cancel"))
        self.noise_method.setText(_translate("AddNoise", "type"))
        self.sample_rate_label.setText(_translate("AddNoise", "sample_rate"))
