# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup
import random

def url_handler(url,headers):
    try:
        r = requests.get(url, headers=headers, timeout=10)#, proxies=proxies)
        soup = BeautifulSoup(r.content, "lxml")
        imgurl = []
        for img in soup('img', 'picact'):
            imgurl.append(img['src'])
        #print imgurl
        download_img(imgurl)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        print "Page No.%d Connectionpool..." % page

def download_img(imgurl):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
               'Referer': 'http://www.gamersky.com/ent/'
               }
    x = 1
    for img in imgurl:
        #proxies = get_proxies()
        try:
            r = requests.get(img, headers=headers, timeout=10)#, proxies=proxies)
            fname = str(n[1])+'_'+str(n[2])+'_'+str(page)+str(x)+img_code+'.jpg'
            print("Downloading No.%s page No.%d picture...")% (page, x)
            x += 1
            with open(fname, 'wb') as f:
                f.write(r.content)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print("Download Connectionpool...")

def get_img_url():#获取首页上最新囧图的网址
    url = 'http://www.gamersky.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
               'Referer': 'http://www.gamersky.com/ent/'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'lxml')
        soup = soup.find('ul', 'Mid7img none')
        s = soup.a['href']
        if len(s) == 24:
            s = 'http://www.gamersky.com' + s

        try:
            with open('img_url.txt', 'r') as f:
                a = f.read()
        except IOError:
            with open('img_url.txt', 'w') as g:
                a = 'null'
                g.write(a)

        if s == a:
            print("The wed not update yet")
            print("Continue to download picture?(y/n)")
            a = raw_input()
            if a == 'y':
                return s
            else:
                return None
        else:
            print("The web has updated")
            with open('img_url.txt', 'w') as f:
                f.write(s)
            return s
    except(requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        print "Get imgurl Connectionpool..."

if __name__ == '__main__':
    n = time.localtime()
    url = get_img_url()#获取最新囧图网址
    img_code = url[35:41:]

    if url:
        page = 1
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
                       'Referer': 'http://www.gamersky.com/ent/'}
        url_handler(url, headers)

        page = 2
        url = url[0:41:]+'_' + str(page) + '.shtml'
        code = 0
        while code < 400:
            try:
                code = requests.get(url, headers=headers, timeout=10).status_code
                url_handler(url, headers)
            except(requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                print "Page No.%d Get StatusCode Connectionpool..." % page
                code = 0
            finally:
                page += 1
                url = url[0:41:]+'_' + str(page) + '.shtml'
                    #print url
                    #print page
                time.sleep(0.5)

    print("Press any key to close:")
    raw_input()
