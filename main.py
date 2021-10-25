from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
import json
from datetime import date
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import csv
import requests
import shutil

def setdriver():
    options = Options()
    options.add_argument("window-size={},{}".format(1920, 1080))
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=options)
    return driver
def getActressesFromWiki(driver):
    driver.get("https://en.wikipedia.org/wiki/List_of_American_film_actresses")
    actressess_eles = driver.find_elements(By.XPATH, '//div[@id="mw-content-text"]/div[@class="mw-parser-output"]/div[@class="div-col"]/ul/li')
    return_array = []
    
    for index, actress_ele in enumerate(actressess_eles, start=1):
        one_dic = {"id":index}
        link_ele = actress_ele.find_element(By.XPATH, 'a[1]')
        one_dic['name'] = link_ele.text
        one_dic['link_url'] = link_ele.get_attribute('href')
        return_array.append(one_dic)
        print(one_dic)
        if index > 30 :
            break
    return return_array
def downloadImageFile(image_url):
    filename = image_url.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')
def getDetailsForActress(actress):
    driver.get(actress['link_url'])
    details_array = driver.find_element(By.XPATH, '//div[@id="mw-content-text"]/div[1]').text.split('\n')[2:30]
    details = []
    for detail in details_array:
        if detail == "Contents":
            break
        details.append(detail)
    actress['details'] = details
    images_eles = driver.find_elements(By.XPATH, '//a[@class="image"]/img')
    for image_ele in images_eles:
        image_url = image_ele.get_attribute('src')
        if not ".jpg" in image_url:
            continue
        else:
            image_thumbnail_url = image_url.split(".jpg")[0]+".jpg"
            image_url = image_thumbnail_url.replace('thumb/', '', 1)
        downloadImageFile(image_url)
    return actress
if __name__ == "__main__":
    driver = setdriver()
    actresses = getActressesFromWiki(driver)
    for actress in actresses:
        actress_details = getDetailsForActress(actress)
        # print(actress_details)

