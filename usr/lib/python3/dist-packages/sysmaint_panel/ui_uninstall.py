


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UninstallDialog(object):
    def setupUi(self, UninstallDialog):
        UninstallDialog.setObjectName("UninstallDialog")
        UninstallDialog.resize(448, 176)
        self.verticalLayout = QtWidgets.QVBoxLayout(UninstallDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(UninstallDialog)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textField = QtWidgets.QLineEdit(UninstallDialog)
        self.textField.setObjectName("textField")
        self.verticalLayout.addWidget(self.textField)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(UninstallDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(UninstallDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(UninstallDialog)
        QtCore.QMetaObject.connectSlotsByName(UninstallDialog)

    def retranslateUi(self, UninstallDialog):
        _translate = QtCore.QCoreApplication.translate
        UninstallDialog.setWindowTitle(_translate("UninstallDialog", "Dialog"))
        self.label.setText(_translate("UninstallDialog", "<p>You are about to uninstall user-sysmaint-split. This will restore<br>normal sudo access for user \'<code>user</code>\'.</p><p>To confirm you really want to do this, type \"<b>yes</b>\" and click OK."))
        self.okButton.setText(_translate("UninstallDialog", "OK"))
        self.cancelButton.setText(_translate("UninstallDialog", "Cancel"))
