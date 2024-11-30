import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog, QGridLayout, QWidget, QApplication, QLineEdit, QCheckBox, QPushButton 
from PyQt5.QtCore import QSize, Qt
import time
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pygame  # Importing pygame

kill_thread = 0
sflag = 1

class dialog(QDialog):
    def closeEvent(self, event):
        browser.quit()

def sendText(s):
    textbox = browser.find_element_by_class_name('_3u328')
    textbox.send_keys(s, Keys.ENTER)

class WASessionsTracker(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)

        self.setFixedSize(QSize(300, 350))
        self.setWindowTitle("WASessionsTracker")

        mainWindow = QWidget(self)
        self.setCentralWidget(mainWindow)

        label1 = QLabel('Target\'s Name :', self)
        label1.setGeometry(30, 30, 71, 16)

        targetname = QLineEdit(self)
        targetname.setGeometry(30, 50, 241, 21)

        start = QPushButton(self)
        start.setGeometry(30, 100, 241, 31)
        start.setText('Start')

        label2 = QLabel('Text :', self)
        label2.setGeometry(30, 140, 71, 16)

        msgbox = QLineEdit(self)
        msgbox.setGeometry(30, 160, 241, 20)

        label3 = QLabel('Send Text', self)
        label3.setGeometry(30, 190, 61, 16)

        checkbox = QCheckBox(self)
        checkbox.setGeometry(260, 190, 41, 20)
        checkbox.setText('')

        targetstatus = QLabel('Status : ', self)
        targetstatus.setGeometry(60, 240, 201, 16)

        AT = QLabel('Came on : ', self)
        AT.setGeometry(60, 270, 201, 16)

        duration = QLabel('Session Duration : ', self)
        duration.setGeometry(60, 300, 201, 16)
        
        def tracker(target):
            user_status = 'offline'
            while True:
                global kill_thread
                if kill_thread:
                    break
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                temp = soup.find('span', class_='_315-i')
                if str(type(temp)) == "<class 'bs4.element.Tag'>":
                    user_status = temp.get_text()
                if user_status == 'online' or user_status == 'typing...':
                    pygame.mixer.init()  # Initialize pygame mixer
                    pygame.mixer.music.load("alert.mp3")  # Load the sound file
                    pygame.mixer.music.play()  # Play the sound
                    targetstatus.setText("Status : " + targetname.text() + " is online!")
                    localtime = time.asctime(time.localtime(time.time()))
                    AT.setText("Came on : " + str(localtime))
                    duration.setText("Session Duration : ")
                    if checkbox.isChecked():
                        sendText(msgbox.text())
                    count = 0
                    while True:
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        temp = soup.find('span', class_='_315-i')
                        if str(type(temp)) != "<class 'bs4.element.Tag'>":
                            duration.setText("Session Duration : " + str(count) + " seconds")
                            user_status = 'offline'
                            targetstatus.setText("Status : " + targetname.text() + " is offline.")
                            break
                        count += 1
                        time.sleep(1)
                    log = open("log.txt", "a")
                    log.write("Target : " + str(target) + "\n")
                    log.write("Came online on : " + str(localtime) + "\n")
                    log.write("Session Duration: " + str(count) + " seconds\n")
                    log.write("------------------------------------------\n")
                    log.close()
                    count = 0
                    
        def startScript():
            global sflag
            global kill_thread
            if sflag:
                t1 = Thread(target=tracker, args=(targetname.text(),))
                targetstatus.setText('Status : Running...')
                start.setText('Stop')
                t1.start()
                sflag = 0
            else:
                kill_thread = 1
                targetstatus.setText('Status : Stopped')
                start.setText('Start')
                sflag = 1
                
        start.clicked.connect(startScript)

    def closeEvent(self, event):
        browser.quit()

def mainwin():
    dialog.hide()
    newInstance.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = dialog()
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
    newInstance = WASessionsTracker()
    browser = webdriver.Chrome()
    browser.get('https://web.whatsapp.com')
    dialog.setWindowTitle("Instructions")
    sys.exit(app.exec_())
