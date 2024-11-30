from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pygame

pygame.mixer.init()

def sendText(s):
    textbox = browser.find_element(By.CLASS_NAME, '_3u328')  # Updated method
    textbox.send_keys(s, Keys.ENTER)

browser = webdriver.Chrome()
browser.get('https://web.whatsapp.com')

print("Step 1. Scan the QR Code.\nStep 2. Open up the chat for the person you want to target.\n")
target = input("Target's Name : ")
print("Running...\n")
user_status = 'offline'
while(True):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    temp = soup.find('span', class_='_315-i')
    if str(type(temp)) == "<class 'bs4.element.Tag'>":
        user_status = temp.get_text()
    if user_status == 'online' or user_status == 'typing...':
        pygame.mixer.music.load("alert.mp3")  # Ensure file exists
        pygame.mixer.music.play()
        count = 0
        print(target, " is online!\n")
        localtime = time.asctime(time.localtime(time.time()))
        print("Came on : ", localtime)
        #sendText("```Automated Text!!```")
        while(True):
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            temp = soup.find('span', class_='_315-i')
            if str(type(temp)) != "<class 'bs4.element.Tag'>":
                user_status = 'offline'
                break
            count = count + 1
            time.sleep(1)
        print("Session Duration: ", count, " seconds\n")
        print("------------------------------------------\n")
        with open("log.txt", "a") as log:
            log.write("Target : " + str(target) + "\n")
            log.write("Came online on : " + str(localtime) + "\n")
            log.write("Session Duration: " + str(count) + " seconds\n")
            log.write("------------------------------------------\n")
        count = 0
