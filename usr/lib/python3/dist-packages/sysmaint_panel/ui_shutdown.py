# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/srv/data/vmshare/kicksecure/git/sysmaint-panel/ui/ui_shutdown.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShutdowDialog(object):
    def setupUi(self, ShutdowDialog):
        ShutdowDialog.setObjectName("ShutdowDialog")
        ShutdowDialog.resize(353, 86)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShutdowDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ShutdowDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.yesButton = QtWidgets.QPushButton(ShutdowDialog)
        self.yesButton.setObjectName("yesButton")
        self.horizontalLayout.addWidget(self.yesButton)
        self.noButton = QtWidgets.QPushButton(ShutdowDialog)
        self.noButton.setObjectName("noButton")
        self.horizontalLayout.addWidget(self.noButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ShutdowDialog)
        QtCore.QMetaObject.connectSlotsByName(ShutdowDialog)

    def retranslateUi(self, ShutdowDialog):
        _translate = QtCore.QCoreApplication.translate
        ShutdowDialog.setWindowTitle(_translate("ShutdowDialog", "Shut Down"))
        self.label.setText(_translate("ShutdowDialog", "Are you sure you want to shut down the system?"))
        self.yesButton.setText(_translate("ShutdowDialog", "Yes"))
        self.noButton.setText(_translate("ShutdowDialog", "No"))
