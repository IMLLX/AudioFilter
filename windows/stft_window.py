# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stft_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_STFT(object):
    def setupUi(self, STFT):
        STFT.setObjectName("STFT")
        STFT.resize(473, 528)
        self.T_value_lable = QtWidgets.QLabel(STFT)
        self.T_value_lable.setGeometry(QtCore.QRect(20, 170, 72, 15))
        self.T_value_lable.setObjectName("T_value_lable")
        self.verticalLayoutWidget = QtWidgets.QWidget(STFT)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 270, 431, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.apply_button = QtWidgets.QPushButton(STFT)
        self.apply_button.setGeometry(QtCore.QRect(340, 80, 93, 28))
        self.apply_button.setObjectName("apply_button")
        self.cancel_button = QtWidgets.QPushButton(STFT)
        self.cancel_button.setGeometry(QtCore.QRect(340, 120, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.window_type_label = QtWidgets.QLabel(STFT)
        self.window_type_label.setGeometry(QtCore.QRect(20, 30, 72, 15))
        self.window_type_label.setObjectName("window_type_label")
        self.window_type_combo = QtWidgets.QComboBox(STFT)
        self.window_type_combo.setGeometry(QtCore.QRect(20, 50, 171, 41))
        self.window_type_combo.setObjectName("window_type_combo")
        self.sample_rate_label = QtWidgets.QLabel(STFT)
        self.sample_rate_label.setGeometry(QtCore.QRect(20, 100, 91, 16))
        self.sample_rate_label.setObjectName("sample_rate_label")
        self.sampe_rate_line = QtWidgets.QLineEdit(STFT)
        self.sampe_rate_line.setGeometry(QtCore.QRect(20, 120, 171, 41))
        self.sampe_rate_line.setObjectName("sampe_rate_line")
        self.T_value_line = QtWidgets.QLineEdit(STFT)
        self.T_value_line.setGeometry(QtCore.QRect(20, 190, 171, 41))
        self.T_value_line.setObjectName("T_value_line")

        self.retranslateUi(STFT)
        QtCore.QMetaObject.connectSlotsByName(STFT)

    def retranslateUi(self, STFT):
        _translate = QtCore.QCoreApplication.translate
        STFT.setWindowTitle(_translate("STFT", "STFT"))
        self.T_value_lable.setText(_translate("STFT", "T"))
        self.apply_button.setText(_translate("STFT", "apply"))
        self.cancel_button.setText(_translate("STFT", "cancel"))
        self.window_type_label.setText(_translate("STFT", "type"))
        self.sample_rate_label.setText(_translate("STFT", "sample_rate"))
