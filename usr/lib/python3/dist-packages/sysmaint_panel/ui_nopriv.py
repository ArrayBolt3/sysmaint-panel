


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NoPrivDialog(object):
    def setupUi(self, NoPrivDialog):
        NoPrivDialog.setObjectName("NoPrivDialog")
        NoPrivDialog.resize(412, 174)
        self.verticalLayout = QtWidgets.QVBoxLayout(NoPrivDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(NoPrivDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(400, 0))
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(NoPrivDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NoPrivDialog)
        QtCore.QMetaObject.connectSlotsByName(NoPrivDialog)

    def retranslateUi(self, NoPrivDialog):
        _translate = QtCore.QCoreApplication.translate
        NoPrivDialog.setWindowTitle(_translate("NoPrivDialog", "Insufficient Privileges"))
        self.label.setText(_translate("NoPrivDialog", "<html><head/><body><p>This system only allows the sysmaint account to perform<br>\n"
"system maintenance. Please reboot and select<br>\n"
"\'PERSISTENT mode SYSMAINT\' at the boot menu.</p>\n"
"<p>See <a href=\"https://www.kicksecure.com/wiki/sysmaint\">https://www.kicksecure.com/wiki/Sysmaint</a> for more<br>\n"
"information.</p></body></html>"))
        self.okButton.setText(_translate("NoPrivDialog", "OK"))
