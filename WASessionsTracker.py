from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pygame
import time

# Specify the path to the Brave browser executable
brave_binary_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Update this if needed

# Specify the path to the chromedriver executable
chrome_driver_path = r"C:\Users\wilio\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Create a Chrome options object and set the Brave binary path
options = Options()
options.binary_location = brave_binary_path  # Set the path to the Brave browser binary

# Create a Service object with the chromedriver path
service = Service(chrome_driver_path)

# Initialize the browser with the service and options
browser = webdriver.Chrome(service=service, options=options)

browser.get('https://web.whatsapp.com')
print("Step 1. Scan the QR Code.\nStep 2. Open up the chat for the person you want to target.\n")
target = input("Target's Name: ")
print("Running...\n")

user_status = 'offline'
while True:
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    temp = soup.find('span', class_='_315-i')

    # Check if user status is available
    if str(type(temp)) == "<class 'bs4.element.Tag'>":
        user_status = temp.get_text()

    if user_status in ('online', 'typing...'):
        pygame.mixer.music.load("alert.mp3")  # Ensure file exists
        pygame.mixer.music.play()
        count = 0
        print(f"{target} is online!\n")
        localtime = time.asctime(time.localtime(time.time()))
        print("Came on: ", localtime)

        # Send automated text (commented out)
        # send_text("```Automated Text!!```")

        while True:
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            temp = soup.find('span', class_='_315-i')

            if str(type(temp)) != "<class 'bs4.element.Tag'>":
                user_status = 'offline'
                break
            count += 1
            time.sleep(1)

        print(f"Session Duration: {count} seconds\n")
        print("------------------------------------------\n")

        # Write session details to the log file
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"Target: {target}\n")
            log.write(f"Came online on: {localtime}\n")
            log.write(f"Session Duration: {count} seconds\n")
            log.write("------------------------------------------\n")

        count = 0
