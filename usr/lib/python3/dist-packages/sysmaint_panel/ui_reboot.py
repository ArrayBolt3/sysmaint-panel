


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RebootDialog(object):
    def setupUi(self, RebootDialog):
        RebootDialog.setObjectName("RebootDialog")
        RebootDialog.resize(326, 86)
        self.verticalLayout = QtWidgets.QVBoxLayout(RebootDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(RebootDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.yesButton = QtWidgets.QPushButton(RebootDialog)
        self.yesButton.setObjectName("yesButton")
        self.horizontalLayout.addWidget(self.yesButton)
        self.noButton = QtWidgets.QPushButton(RebootDialog)
        self.noButton.setObjectName("noButton")
        self.horizontalLayout.addWidget(self.noButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RebootDialog)
        QtCore.QMetaObject.connectSlotsByName(RebootDialog)

    def retranslateUi(self, RebootDialog):
        _translate = QtCore.QCoreApplication.translate
        RebootDialog.setWindowTitle(_translate("RebootDialog", "Reboot"))
        self.label.setText(_translate("RebootDialog", "Are you sure you want to reboot the system?"))
        self.yesButton.setText(_translate("RebootDialog", "Yes"))
        self.noButton.setText(_translate("RebootDialog", "No"))
