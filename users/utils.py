import json
import os
import threading

from time import sleep
import requests
import validators
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from youtubesearchpython import VideosSearch

from math import floor, ceil

import nltk
from nltk import FreqDist
from nltk.corpus import stopwords

img_dict = {}
import webbrowser
from time import sleep

import selenium
import validators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# inpu = ""



def var(topic):
    inpu = topic.replace(" ", "+")
    return inpu


def i_search(inpu):
    drive = webdriver.Chrome(r"C:\Users\Admin\Desktop\SOMA\users\chromedriver.exe")
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
    drive = webdriver.Chrome(r"C:\Users\Admin\Desktop\SOMA\users\chromedriver.exe")
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


def get_youtube_url(query):
    videosSearch = VideosSearch(query, limit=4)
    links = []
    d = videosSearch.result()["result"]
    for i in d:
        links.append(i["link"])

    return links


def se_arch(que_ry):
    return {"youtube": get_youtube_url(que_ry), "google": search_(que_ry), "images": i_search(que_ry)}


# MAIN FUNCTION START
def main(url):
    # content of URL
    r = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')

    # find all images in URL
    images = soup.findAll('img')
    # Call folder create function
    download_images(images, url)


def download_images(images, url):
    # initial count is zero
    count = 0
    # print total images found in URL
    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            loop_image(image, url)


def loop_image(image, url):
    global count, img_dict
    count = 0
    li = ""
    image_link = ""
    try:
        # In image tag ,searching for "data-srcset"
        image_link = image["data-srcset"]

    # then we will search for "data-src" in img
    # tag and so on..
    except:
        try:
            # In image tag ,searching for "data-src"
            image_link = image["data-src"]
        except:
            try:
                # In image tag ,searching for "data-fallback-src"
                image_link = image["data-fallback-src"]
            except:
                try:
                    # In image tag ,searching for "src"
                    image_link = image["src"]

                # if no Source URL found
                except:
                    pass
    # From image tag ,Fetch image Source URL

    # 1.data-srcset
    # 2.data-src
    # 3.data-fallback-src
    # 4.src

    # Here we will use exception handling
    if not validators.url(image_link):
        image_link = url + image_link
    try:
        name = image["alt"]
    except:
        li = image_link.split("://")[1]
        name = li

    img_dict[name] = image_link

    # After getting Image Source URL
    # We will try to get the content of image

    # After checking above condition, Image Download start

    # There might be possible, that all
    # images not download
    # if all images download


# first we will search for "data-srcset" in img tag

def word_return(text):
    p = [t for t in nltk.tag.pos_tag(nltk.word_tokenize(text)) if t[1] == "NN"]

    words = [i[0] for i in p if
             not (len(i[0]) << 3 and not i[0].isalnum())]
    words = [w for w in words if w.lower() not in set(stopwords.words("english"))]
    words = FreqDist(word.lower() for word in words)
    print(words.most_common())
    return words.most_common()


def g_search(query):
    articles = {}

    url = f"https://google-search3.p.rapidapi.com/api/v1/search/q={query}"

    headers = {
        'x-user-agent': "desktop",
        'x-proxy-location': "EU",
        'x-rapidapi-host': "google-search3.p.rapidapi.com",
        'x-rapidapi-key': "49455f7e26msh7387d38ba4e0f4bp13f66cjsnca053141077d"
    }
    response = requests.request("GET", url, headers=headers)

    j = json.loads(response.text)
    print(j)
    for i in range(4):
        print(j["results"][0]["title"])
        articles[str(j["results"][i]["title"]).strip()] = j["results"][i]["link"]
    print(articles)
    return articles


def g_img_search(query):
    global img_dict
    img_dict = {}
    url = f"https://google-search3.p.rapidapi.com/api/v1/images/q={query}"

    headers = {
        'x-user-agent': "desktop",
        'x-proxy-location': "EU",
        'x-rapidapi-host': "google-search3.p.rapidapi.com",
        'x-rapidapi-key': "49455f7e26msh7387d38ba4e0f4bp13f66cjsnca053141077d"
    }
    response = requests.request("GET", url, headers=headers)

    j = json.loads(response.text)
    print(j)
    l = list(j["image_results"])
    print(l[0]["image"]["src"])
    src = []
    i = 0
    while True:

        if l[i]["image"]["src"] not in src:
            src.append(l[i]["image"]["src"])
            if l[i]["image"]["alt"] == "":
                img_dict[i] = l[i]["image"]["src"]
            else:
                img_dict[str(l[i]["image"]["alt"]).strip()] = l[i]["image"]["src"]
            i += 1
        if i == 5:
            break

    print(img_dict)
    return img_dict
