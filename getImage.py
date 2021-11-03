import csv
import json
import urllib.request
import os
import os.path

IMGFOLDER = os.getcwd() + '/images/'

def readimg(url):
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return response.read()

with open('result.csv', mode='r', encoding='utf-8') as result_file:
    csv_reader = csv.DictReader(result_file)
    for actress in csv_reader:
        photos_urls = actress['photos'].strip('][').split(', ')
        for index, url in enumerate(photos_urls, start=1):
            url = url.strip("'")
            print(url)
            if url == "":
                continue
            try:
                file_name = IMGFOLDER + actress['id']+'_'+actress['name']+'_'+str(index) +'.jpg'
                if os.path.isfile(file_name):
                    continue
                with urllib.request.urlopen(url) as response:
                    if response.status == 200:
                        with open(file_name, 'wb') as f:
                            f.write(readimg(url))
            except Exception as e:
                print(e)
                continue