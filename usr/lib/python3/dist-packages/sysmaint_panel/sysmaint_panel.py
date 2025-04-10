#!/usr/bin/python3 -u

# Copyright (C) 2024 - 2025 ENCRYPTED SUPPORT LLC <adrelanos@kicksecure.com>
## See the file COPYING for copying conditions.

import sys
import subprocess
import os
import grp
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QTimer
from PyQt5.QtGui import QPixmap

from sysmaint_panel.ui_mainwindow import Ui_MainWindow
from sysmaint_panel.ui_reboot import Ui_RebootDialog
from sysmaint_panel.ui_shutdown import Ui_ShutdownDialog
from sysmaint_panel.ui_managesoftware import Ui_ManageSoftwareDialog
from sysmaint_panel.ui_managesoftwarehelp import Ui_ManageSoftwareHelpDialog
from sysmaint_panel.ui_background import Ui_BackgroundScreen
from sysmaint_panel.ui_nopriv import Ui_NoPrivDialog
from sysmaint_panel.ui_wronguser import Ui_WrongUserDialog
from sysmaint_panel.ui_uninstall import Ui_UninstallDialog

# from ui_mainwindow import Ui_MainWindow
# from ui_reboot import Ui_RebootDialog
# from ui_shutdown import Ui_ShutdownDialog
# from ui_managesoftware import Ui_ManageSoftwareDialog
# from ui_managesoftwarehelp import Ui_ManageSoftwareHelpDialog
# from ui_background import Ui_BackgroundScreen
# from ui_nopriv import Ui_NoPrivDialog
# from ui_wronguser import Ui_WrongUserDialog
# from ui_uninstall import Ui_UninstallDialog

# Honor sigterm
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


def is_qubes_os():
    return Path("/usr/share/qubes/marker-vm").exists()

def timeout_lock(button):
    button_text_parts = button.text().split(" ")
    button_text_end_number = button_text_parts[
        len(button_text_parts) - 1
    ].strip("()")

    try:
        button_unlock_time = int(button_text_end_number)
    except Exception:
        button_text_parts.append("(5)")
        button.setText(" ".join(button_text_parts))
        button.setEnabled(False)
        QTimer.singleShot(1000, lambda: timeout_lock(button))
        return

    button_text_parts.pop()
    button_unlock_time -= 1
    if button_unlock_time == 0:
        button.setText(" ".join(button_text_parts))
        button.setEnabled(True)
        return

    button_text_parts.append(f"({button_unlock_time})")
    button.setText(" ".join(button_text_parts))
    QTimer.singleShot(1000, lambda: timeout_lock(button))


class NoPrivDialog(QDialog):
    def __init__(self):
        super(NoPrivDialog, self).__init__()
        self.ui = Ui_NoPrivDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.okButton.clicked.connect(self.done)


class WrongUserDialog(QDialog):
    def __init__(self):
        super(WrongUserDialog, self).__init__()
        self.ui = Ui_WrongUserDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.okButton.clicked.connect(self.done)


class BackgroundScreen(QDialog):
    def __init__(self):
        super(BackgroundScreen, self).__init__()
        self.ui = Ui_BackgroundScreen()
        self.ui.setupUi(self)


class ManageSoftwareHelpDialog(QDialog):
    def __init__(self):
        super(ManageSoftwareHelpDialog, self).__init__()
        self.ui = Ui_ManageSoftwareHelpDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.okButton.clicked.connect(self.done)


class ManageSoftwareDialog(QDialog):
    def __init__(self):
        super(ManageSoftwareDialog, self).__init__()
        self.ui = Ui_ManageSoftwareDialog()
        self.ui.setupUi(self)
        self.resize(self.minimumWidth(), self.minimumHeight())

        self.ui.runButton.clicked.connect(self.run_action)
        self.ui.cancelButton.clicked.connect(self.cancel)

    def run_action(self):
        match self.ui.actionComboBox.currentText():
            case "Search":
                subprocess.Popen(
                    [
                        "/usr/libexec/helper-scripts/terminal-wrapper",
                        "/usr/bin/apt-cache",
                        "search",
                        self.ui.packageLineEdit.text(),
                    ]
                )
            case "Install":
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
            case "Reinstall":
                subprocess.Popen(
                    [
                        "/usr/libexec/helper-scripts/terminal-wrapper",
                        "/usr/bin/sudo",
                        "/usr/bin/apt-get-reset",
                        self.ui.packageLineEdit.text(),
                    ]
                )
                self.done(0)
            case "Remove":
                subprocess.Popen(
                    [
                        "/usr/libexec/helper-scripts/terminal-wrapper",
                        "/usr/bin/sudo",
                        "/usr/bin/apt",
                        "remove",
                        self.ui.packageLineEdit.text(),
                    ]
                )
                self.done(0)
            case "Purge":
                subprocess.Popen(
                    [
                        "/usr/libexec/helper-scripts/terminal-wrapper",
                        "/usr/bin/sudo",
                        "/usr/bin/apt",
                        "purge",
                        self.ui.packageLineEdit.text(),
                    ]
                )
                self.done(0)
            case "Override":
                subprocess.Popen(
                    [
                        "/usr/libexec/helper-scripts/terminal-wrapper",
                        "/usr/bin/sudo",
                        "/usr/bin/dummy-dependency",
                        "--remove",
                        self.ui.packageLineEdit.text(),
                    ]
                )
                self.done(0)
            case "Help":
                help_window = ManageSoftwareHelpDialog()
                help_window.exec()

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
        if xdg_current_desktop.startswith("sysmaint-session"):
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

        self.detect_live_mode()

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
        self.ui.manageSoftwareButton.clicked.connect(self.manage_software)

        self.ui.openTerminalButton.clicked.connect(self.open_terminal)
        self.ui.lockScreenButton.clicked.connect(self.lock_screen)
        self.ui.rebootButton.clicked.connect(self.reboot)
        self.ui.shutDownButton.clicked.connect(self.shutdown)

    closed = pyqtSignal()

    # Overrides QMainWindow.closeEvent
    def closeEvent(self, e):
        if xdg_current_desktop.startswith("sysmaint-session") and not is_qubes_os():
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
            if xdg_current_desktop.startswith("sysmaint-session"):
                e.ignore()
                self.setWindowState(e.oldState())
                return True

        return super(MainWindow, self).event(e)

    def detect_live_mode(self):
        base_icon_dir = "/usr/share/icons/gnome-colors-common/32x32"
        live_mode_str = subprocess.run(
            [
                "/usr/bin/bash",
                "-c",
                "eval \"$(/usr/libexec/helper-scripts/live-mode.sh)\"; "
                + "echo "
                + "\"$live_status_detected_live_mode_environment_machine\""
            ],
            capture_output = True,
            text = True,
        ).stdout.strip()
        match live_mode_str:
            case "iso-live":
                self.ui.bootModeIconLabel.setPixmap(
                    QPixmap(base_icon_dir + "/devices/media-optical.png")
                )
                self.ui.bootModeNameLabel.setText("ISO Live Mode")
            case "grub-live":
                self.ui.bootModeIconLabel.setPixmap(
                    QPixmap(base_icon_dir + "/status/user-online.png")
                )
                self.ui.bootModeNameLabel.setText("grub-live Mode")
            case "false":
                self.ui.bootModeIconLabel.setPixmap(
                    QPixmap(base_icon_dir + "/status/dialog-information.png")
                )
                self.ui.bootModeNameLabel.setText("Persistent Mode")
            case _:
                self.ui.bootModeIconLabel.setPixmap(
                    QPixmap(base_icon_dir + "/status/dialog-error.png")
                )
                self.ui.bootModeNameLabel.setText("Error getting boot mode")

    def install_system(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/install-host",
            ]
        )
        timeout_lock(self.ui.installSystemButton)

    def check_for_updates(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/libexec/security-misc/apt-get-update",
            ]
        )
        timeout_lock(self.ui.checkForUpdatesButton)

    def install_updates(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/upgrade-nonroot",
            ]
        )
        timeout_lock(self.ui.installUpdatesButton)

    def remove_unused_packages(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "autoremove",
            ]
        )
        timeout_lock(self.ui.removeUnusedPackagesButton)

    def purge_unused_packages(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/bin/apt",
                "autopurge",
            ]
        )
        timeout_lock(self.ui.purgeUnusedPackagesButton)

    @staticmethod
    def manage_software():
        manage_software_window = ManageSoftwareDialog()
        manage_software_window.exec()

    def manage_passwords(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/sbin/pwchange",
            ]
        )
        timeout_lock(self.ui.managePasswordsButton)

    def create_user(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/libexec/sysmaint-panel/create-user",
            ]
        )
        timeout_lock(self.ui.createUserButton)

    def remove_user(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/sbin/deluser",
            ]
        )
        timeout_lock(self.ui.removeUserButton)

    def manage_autologin(self):
        subprocess.Popen(
            [
                "/usr/libexec/helper-scripts/terminal-wrapper",
                "/usr/bin/sudo",
                "/usr/sbin/autologinchange",
            ]
        )
        timeout_lock(self.ui.manageAutologinButton)

    def check_system_status(self):
        subprocess.Popen(["/usr/bin/systemcheck", "--gui"])
        timeout_lock(self.ui.checkSystemStatusButton)

    @staticmethod
    def open_terminal():
        subprocess.Popen(
            ["/usr/libexec/helper-scripts/terminal-wrapper", default_shell]
        )

    def lock_screen(self):
        subprocess.Popen(["/usr/libexec/helper-scripts/lock-screen"])
        timeout_lock(self.ui.lockScreenButton)

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
            if "boot-role=sysmaint" in kernel_cmdline:
                wuwin = WrongUserDialog()
                wuwin.show()
            else:
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
        if is_qubes_os():
            window.ui.rebootButton.setVisible(False)

    window.show()

    if xdg_current_desktop.startswith("sysmaint-session") and not is_qubes_os():
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
