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
import os
IMGFOLDER = os.getcwd() + '/images/'


class BingImage(object):
    """docstring for BingImage"""
    BINGURL = 'http://www.bing.com/'
    JSONURL = 'HPImageArchive.aspx?format=js&idx=0&n=1&mkt=pt-BR'
    LASTIMG = None

    def __init__(self):
        super(BingImage, self).__init__()
        try:
            self.downloadimg()
        except:
            pass
    def setURL(self, URL):
        self.URL = URL
    def getdailyimg(self):
        import json
        import urllib.request
        with urllib.request.urlopen(self.URL) as response:
            rawjson = response.read().decode('utf-8')
            parsedjson = json.loads(rawjson)
            return self.BINGURL + parsedjson['images'][0]['url'][1:]

    def downloadimg(self):
        import datetime
        imgurl = self.getdailyimg()
        imgfilename = datetime.datetime.today().strftime('%Y%m%d') + '_' + imgurl.split('/')[-1]
        with open(IMGFOLDER + imgfilename, 'wb') as f:
            f.write(self.readimg(imgurl))
        self.LASTIMG = IMGFOLDER + imgfilename

    def checkfolder(self):
        d = os.path.dirname(IMGFOLDER)
        if not os.path.exists(d):
            os.makedirs(d)

    def readimg(self, url):
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return response.read()


def DefineBackground(src):
    import platform
    if platform.system() == 'Linux':
        MAINCMD = "gsettings set org.gnome.desktop.background picture-uri"
        os.system(MAINCMD + ' file://' + src)


def GetRandomImg():
    """Return a random image already downloaded from the images folder"""
    import random
    f = []
    for (dirpath, dirnames, filenames) in os.walk(IMGFOLDER):
        f.extend(filenames)
        break
    return IMGFOLDER + random.choice(f)


if __name__ == '__main__':
    # get a new today's image from Bing
    img = BingImage()
    
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
        # if index>5:
        #     break
       
    return return_array
def downloadImageFile(image_url, actress, image_count):
    
    filename = image_url.split("/")[-1]

    r = requests.get(image_url, stream = True)
    sleep(3)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open('images/'+str(actress['id'])+'_' + str(image_count) + '_'+filename,'wb') as f:
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
    image_count = 1
    photos = []
    for image_ele in images_eles:
        image_url = image_ele.get_attribute('src')
        if not ".jpg" in image_url:
            continue
        else:
            image_thumbnail_url = image_url.split(".jpg")[0]+".jpg"
            image_url = image_thumbnail_url.replace('thumb/', '', 1)
        photos.append(image_url)
        # downloadImageFile(image_url, actress, image_count)

        image_count += 1
    actress['photos'] = photos
    return actress
if __name__ == "__main__":

    # img = BingImage()
    driver = setdriver()
    actresses = getActressesFromWiki(driver)
    
    with open('result.csv', mode='w', encoding='utf-8') as result_file:
        csv_writer = csv.DictWriter(result_file, fieldnames=list(actresses[0].keys())+['details','photos'])
        csv_writer.writeheader()
        for actress in actresses:
            actress_details = getDetailsForActress(actress)
            csv_writer.writerow(actress_details)

