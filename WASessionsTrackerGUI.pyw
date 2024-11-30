import sys
import time
from threading import Thread
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog, QLineEdit, QCheckBox, QPushButton, QWidget, QApplication
from PyQt5.QtCore import QSize, Qt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pygame

# Initialize pygame mixer
pygame.mixer.init()

class Dialog(QDialog):
    def closeEvent(self, event):
        browser.quit()

class WASessionsTracker(QMainWindow):
    def __init__(self):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.setFixedSize(QSize(300, 350))
        self.setWindowTitle("WASessionsTracker")

        self.kill_thread = False
        self.sflag = True

        # Main window setup
        mainWindow = QWidget(self)
        self.setCentralWidget(mainWindow)

        # Target name input
        label1 = QLabel('Target\'s Name :', self)
        label1.setGeometry(30, 30, 71, 16)

        self.targetname = QLineEdit(self)
        self.targetname.setGeometry(30, 50, 241, 21)

        # Start/Stop button
        self.start_button = QPushButton(self)
        self.start_button.setGeometry(30, 100, 241, 31)
        self.start_button.setText('Start')

        # Message input
        label2 = QLabel('Text :', self)
        label2.setGeometry(30, 140, 71, 16)

        self.msgbox = QLineEdit(self)
        self.msgbox.setGeometry(30, 160, 241, 20)

        # Send text checkbox
        label3 = QLabel('Send Text', self)
        label3.setGeometry(30, 190, 61, 16)

        self.checkbox = QCheckBox(self)
        self.checkbox.setGeometry(260, 190, 41, 20)

        # Status labels
        self.targetstatus = QLabel('Status : ', self)
        self.targetstatus.setGeometry(60, 240, 201, 16)

        self.AT = QLabel('Came on : ', self)
        self.AT.setGeometry(60, 270, 201, 16)

        self.duration = QLabel('Session Duration : ', self)
        self.duration.setGeometry(60, 300, 201, 16)

        # Start/Stop script handler
        self.start_button.clicked.connect(self.start_script)

    def send_text(self, text):
        """Send the specified text to the target WhatsApp user."""
        textbox = browser.find_element_by_class_name('_3u328')
        textbox.send_keys(text, Keys.ENTER)

    def tracker(self, target):
        """Track target's online status and manage session."""
        user_status = 'offline'
        while True:
            if self.kill_thread:
                break

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            temp = soup.find('span', class_='_315-i')

            if str(type(temp)) == "<class 'bs4.element.Tag'>":
                user_status = temp.get_text()

            if user_status in ('online', 'typing...'):
                pygame.mixer.music.load("alert.mp3")
                pygame.mixer.music.play()

                self.targetstatus.setText(f"Status : {self.targetname.text()} is online!")
                localtime = time.asctime(time.localtime(time.time()))
                self.AT.setText(f"Came on : {localtime}")
                self.duration.setText("Session Duration : ")

                if self.checkbox.isChecked():
                    self.send_text(self.msgbox.text())

                count = 0
                while True:
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    temp = soup.find('span', class_='_315-i')

                    if str(type(temp)) != "<class 'bs4.element.Tag'>":
                        self.duration.setText(f"Session Duration : {count} seconds")
                        user_status = 'offline'
                        self.targetstatus.setText(f"Status : {self.targetname.text()} is offline.")
                        break

                    count += 1
                    time.sleep(1)

                with open("log.txt", "a", encoding="utf-8") as log:
                    log.write(f"Target : {target}\n")
                    log.write(f"Came online on : {localtime}\n")
                    log.write(f"Session Duration: {count} seconds\n")
                    log.write("------------------------------------------\n")

                count = 0

    def start_script(self):
        """Start or stop the session tracker based on the current flag."""
        if self.sflag:
            self.kill_thread = False
            target = self.targetname.text()
            self.targetstatus.setText('Status : Running...')
            self.start_button.setText('Stop')

            t1 = Thread(target=self.tracker, args=(target,))
            t1.start()

            self.sflag = False
        else:
            self.kill_thread = True
            self.targetstatus.setText('Status : Stopped')
            self.start_button.setText('Start')
            self.sflag = True

    def closeEvent(self, event):
        """Ensure the browser is closed when the application is closed."""
        browser.quit()

def mainwin():
    dialog.hide()
    new_instance.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    dialog = Dialog()
    bt = QPushButton("OK", dialog)
    bt.move(377, 70)
    dialog.setFixedSize(QSize(480, 120))
    dialog.setWindowTitle("Loading...")

    l1 = QLabel("Step 1. Scan the QR Code.", dialog)
    l1.move(40, 33)
    l2 = QLabel("Step 2. Open up the chat for the person you want to target.", dialog)
    l2.move(40, 73)

    bt.clicked.connect(mainwin)
    dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
    dialog.show()

    new_instance = WASessionsTracker()

    # Launch the browser
    browser = webdriver.Chrome()
    browser.get('https://web.whatsapp.com')

    dialog.setWindowTitle("Instructions")
    sys.exit(app.exec_())
