#!/usr/bin/python3 -u

# Copyright (C) 2024 - 2025 ENCRYPTED SUPPORT LLC <adrelanos@kicksecure.com>
## See the file COPYING for copying conditions.

import sys
import subprocess
import os
import grp

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QProcess

from sysmaint_panel.ui_mainwindow import Ui_MainWindow
from sysmaint_panel.ui_reboot import Ui_RebootDialog
from sysmaint_panel.ui_shutdown import Ui_ShutdownDialog
from sysmaint_panel.ui_installsoftware import Ui_InstallSoftwareDialog
from sysmaint_panel.ui_background import Ui_BackgroundScreen
from sysmaint_panel.ui_nopriv import Ui_NoPrivDialog
from sysmaint_panel.ui_uninstall import Ui_UninstallDialog

# from ui_mainwindow import Ui_MainWindow
# from ui_reboot import Ui_RebootDialog
# from ui_shutdown import Ui_ShutdownDialog
# from ui_installsoftware import Ui_InstallSoftwareDialog
# from ui_background import Ui_BackgroundScreen
# from ui_nopriv import Ui_NoPrivDialog
# from ui_uninstall import Ui_UninstallDialog

# Honor sigterm
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


class NoPrivDialog(QDialog):
    def __init__(self):
        super(NoPrivDialog, self).__init__()
        self.ui = Ui_NoPrivDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.okButton.clicked.connect(self.done)


class BackgroundScreen(QDialog):
    def __init__(self):
        super(BackgroundScreen, self).__init__()
        self.ui = Ui_BackgroundScreen()
        self.ui.setupUi(self)


class InstallSoftwareDialog(QDialog):
    def __init__(self):
        super(InstallSoftwareDialog, self).__init__()
        self.ui = Ui_InstallSoftwareDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.searchButton.clicked.connect(self.search_for_package)
        self.ui.installButton.clicked.connect(self.install_package)
        self.ui.cancelButton.clicked.connect(self.cancel)

    def search_for_package(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/apt-cache",
                "search",
                self.ui.packageLineEdit.text(),
            ]
        )
        print(1)

    def install_package(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "install",
                self.ui.packageLineEdit.text(),
            ]
        )
        self.done(0)

    def cancel(self):
        self.done(0)


class RebootWindow(QDialog):
    def __init__(self):
        super(RebootWindow, self).__init__()
        self.ui = Ui_RebootDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.yesButton.clicked.connect(self.reboot)
        self.ui.noButton.clicked.connect(self.cancel)

    @staticmethod
    def reboot():
        subprocess.run(["/usr/sbin/reboot"])

    def cancel(self):
        self.done(0)


class ShutdownWindow(QDialog):
    def __init__(self):
        super(ShutdownWindow, self).__init__()
        self.ui = Ui_ShutdownDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.yesButton.clicked.connect(self.shutdown)
        self.ui.noButton.clicked.connect(self.cancel)

    @staticmethod
    def shutdown():
        subprocess.run(["/usr/sbin/shutdown", "now"])

    def cancel(self):
        self.done(0)


class UninstallDialog(QDialog):
    def __init__(self):
        super(UninstallDialog, self).__init__()
        self.ui = Ui_UninstallDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())
        self.ui.okButton.setEnabled(False)

        self.ui.okButton.clicked.connect(self.uninstall)
        self.ui.cancelButton.clicked.connect(self.cancel)
        self.ui.textField.textEdited.connect(self.check_text)

    closed = pyqtSignal()

    # Overrides QMainWindow.closeEvent
    def closeEvent(self, e):
        if xdg_current_desktop == "sysmaint-session":
            e.ignore()
            self.cancel()
        else:
            # noinspection PyUnresolvedReferences
            self.closed.emit()

    def check_text(self, text):
        if text == "yes":
            self.ui.okButton.setEnabled(True)
        else:
            self.ui.okButton.setEnabled(False)

    @staticmethod
    def uninstall():
        subprocess.run(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/dummy-dependency",
                "--yes",
                "--purge",
                "user-sysmaint-split",
            ]
        )
        subprocess.run(["/usr/sbin/reboot"])

    @staticmethod
    def cancel():
        subprocess.run(["/usr/sbin/reboot"])


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.installSystemButton.clicked.connect(self.install_system)

        self.ui.checkForUpdatesButton.clicked.connect(self.check_for_updates)
        self.ui.installUpdatesButton.clicked.connect(self.install_updates)
        self.ui.removeUnusedPackagesButton.clicked.connect(
            self.remove_unused_packages
        )
        self.ui.purgeUnusedPackagesButton.clicked.connect(
            self.purge_unused_packages
        )

        self.ui.managePasswordsButton.clicked.connect(self.manage_passwords)
        self.ui.manageAutologinButton.clicked.connect(self.manage_autologin)
        self.ui.checkSystemStatusButton.clicked.connect(
            self.check_system_status
        )
        self.ui.createUserButton.clicked.connect(self.create_user)
        self.ui.removeUserButton.clicked.connect(self.remove_user)
        self.ui.installSoftwareButton.clicked.connect(self.install_software)

        self.ui.openTerminalButton.clicked.connect(self.open_terminal)
        self.ui.rebootButton.clicked.connect(self.reboot)
        self.ui.shutDownButton.clicked.connect(self.shutdown)

    closed = pyqtSignal()

    # Overrides QMainWindow.closeEvent
    def closeEvent(self, e):
        if xdg_current_desktop == "sysmaint-session":
            e.ignore()
            shutdown_window = ShutdownWindow()
            shutdown_window.exec()
        else:
            # noinspection PyUnresolvedReferences
            self.closed.emit()

    # Overrides QMainWindow.event
    def event(self, e):
        if (
            e.type() == QEvent.WindowStateChange
            and (self.windowState() & Qt.WindowMinimized) == Qt.WindowMinimized
        ):
            if xdg_current_desktop == "sysmaint-session":
                e.ignore()
                self.setWindowState(e.oldState())
                return True

        return super(MainWindow, self).event(e)

    @staticmethod
    def install_system():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/install-host",
            ]
        )

    @staticmethod
    def check_for_updates():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "update",
            ]
        )

    @staticmethod
    def install_updates():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "full-upgrade",
            ]
        )

    @staticmethod
    def remove_unused_packages():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "autoremove",
            ]
        )

    @staticmethod
    def purge_unused_packages():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "autopurge",
            ]
        )

    @staticmethod
    def install_software():
        install_software_window = InstallSoftwareDialog()
        install_software_window.exec()

    @staticmethod
    def manage_passwords():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/sbin/pwchange",
            ]
        )

    @staticmethod
    def create_user():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/libexec/sysmaint-panel/create-user",
            ]
        )

    @staticmethod
    def remove_user():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/sbin/deluser",
            ]
        )

    @staticmethod
    def manage_autologin():
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/sbin/autologinchange",
            ]
        )

    @staticmethod
    def check_system_status():
        subprocess.Popen(["/usr/bin/systemcheck"])

    @staticmethod
    def open_terminal():
        subprocess.Popen(
            ["/usr/libexec/helper-scripts/terminal-wrapper", default_shell]
        )

    @staticmethod
    def reboot():
        reboot_window = RebootWindow()
        reboot_window.exec()

    @staticmethod
    def shutdown():
        shutdown_window = ShutdownWindow()
        shutdown_window.exec()


def main():
    app = QApplication(sys.argv)

    sudo_stat_info = os.stat("/usr/bin/sudo")
    sudo_owning_gid = sudo_stat_info.st_gid
    sudo_owning_group = grp.getgrgid(sudo_owning_gid)[0]
    if sudo_owning_group == "sysmaint":
        if not os.access("/usr/bin/sudo", os.X_OK):
            npwin = NoPrivDialog()
            npwin.show()
            sys.exit(app.exec_())

    if "remove-sysmaint" in kernel_cmdline:
        window = UninstallDialog()
    else:
        window = MainWindow()
        if (
            not "rd.live.image" in kernel_cmdline
            and not "remove-sysmaint" in kernel_cmdline
        ):
            window.ui.installationGroupBox.setVisible(False)

    window.show()

    if xdg_current_desktop == "sysmaint-session":
        bgrd_list = []
        for screen in app.screens():
            bgrd = BackgroundScreen()
            bgrd.setGeometry(screen.geometry())
            bgrd.setWindowFlags(
                Qt.WindowStaysOnBottomHint | Qt.WindowDoesNotAcceptFocus
            )
            bgrd.showFullScreen()
            # noinspection PyUnresolvedReferences
            window.closed.connect(bgrd.close)
            bgrd_list.append(bgrd)

    sys.exit(app.exec_())


xdg_current_desktop = ""
if "XDG_CURRENT_DESKTOP" in os.environ:
    xdg_current_desktop = os.environ["XDG_CURRENT_DESKTOP"]
default_shell = "/bin/bash"
if "SHELL" in os.environ:
    default_shell = os.environ["SHELL"]

with open("/proc/cmdline", "r") as kernel_cmdline_file:
    kernel_cmdline = kernel_cmdline_file.read()

if __name__ == "__main__":
    main()
