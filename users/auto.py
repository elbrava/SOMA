import webbrowser
from time import sleep

import selenium
import validators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# inpu = ""
drive = webdriver.Chrome("chromedriver.exe")


def var(topic):
    inpu = topic.replace(" ", "+")
    return inpu


def i_search(inpu):
    inpu = var(inpu)
    drive.implicitly_wait(4)
    try:
        drive.get("https://www.google.com/search?q=" + inpu + "&start" + str(1))
        drive.implicitly_wait(3)
        a = drive.find_element(By.XPATH, "//*[@id='hdtb-msb']/div[1]/div/div[2]/a")
        v = a.get_attribute("href")
        a.click()
        images = drive.find_elements(By.TAG_NAME, "img")
        images = [u.get_attribute("src") for u in images]
        images = [u for u in images if u != None]
        drive.implicitly_wait(3)

        _ = [print(u) for u in images]
        return
    except Exception as e:
        print(e)
        i_search(inpu)


def search_(inpu):
    inpu = var(inpu)
    try:
        drive.get("https://www.google.com/search?q=" + inpu + "&start" + str(1))
        drive.implicitly_wait(3)
        a = drive.find_elements(By.TAG_NAME, "a")
        a = [e.get_attribute("href") for e in a]
        a = [e for e in a if e is not None]
        print(len(a))
        _ = [print(e) for e in a if not e.__contains__("google")]
        print(len(a))
    except Exception as e:
        search_(inpu)
