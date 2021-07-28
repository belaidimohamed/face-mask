# normal downloader given us a > 91% of duplicate images , which is very bad let's try to build a smarter one :D
import base64
from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from Blocks.duplicate import Duplicate
from PIL import Image
import base64
from PIL import Image
from io import BytesIO
import numpy as np

class SmartDownloader():
    def __init__(self,config):
        self.config = config  # config comming from download.yaml
        self.removed = 0    # numbers of duplicate image removed before downloading
        self.hashes = set() # a set of hashed images to check duplicates

        self.browser = None # control the chrome page
        self.scroll = 0    # scrolled pixels
        self.downloaded = 0 # how many images downloaded
        #  search engines to scrap until the number of images downloaded is the same as demanded
        self.search_engine = ['google','yahoo','bing','duckduckgo']
        self.search_engine_index = 0 # current search engine index

    def crowl(self):
        if(self.browser == None):
            self.browser = webdriver.Chrome("Assets/chromedriver") #incase you are chrome
        if(self.search_engine[self.search_engine_index]=='google'):
            self.crowl_Google()
        if(self.search_engine[self.search_engine_index]=='yahoo'):
            self.crowl_Yahoo()
        else :
            print('Sorry we are out of search engines ! \n Try adding more different keywords')

    def crowl_Yahoo(self):
        self.browser.get("https://search.yahoo.com/")
        search = self.browser.find_element_by_name("p")
        search.send_keys(self.config['search_key'] , Keys.ENTER)
        elem = self.browser.find_element_by_link_text("Images")
        elem.get_attribute("href")
        elem.click()

        number_of_images = self.config['image_numbers'] - self.downloaded
        self.sub = set()
        self.scroll = 0
        old_sub_len = 0
        same_len = 0 # check if there is no more new images
        while len(self.sub) <= number_of_images and same_len <8 :
            self.browser.execute_script("scrollBy(0,"+ str(self.scroll) +");")
            self.scroll += 950
            time.sleep(1)
            elem1 = self.browser.find_elements_by_xpath('//img[contains(@id, yui)]')
            self.sub.update(elem1)
            if(len(self.sub)==old_sub_len):
                same_len +=1
            else :
                old_sub_len = len(self.sub)
                same_len = 0
            print(str(len(self.sub))+'---- ' + str(same_len))
            try:
                show_more = self.browser.find_elements_by_xpath("//button[contains(@class, ygbt.more-res)][@name='more-res']")
                show_more[0].click()
            except:
                pass
        self.download()

    def crowl_Google(self):
        self.browser.get("https://www.google.com/?hl=en")
        search = self.browser.find_element_by_name("q")
        search.send_keys(self.config['search_key'] , Keys.ENTER)
        elem = self.browser.find_element_by_link_text("Images")
        elem.get_attribute("href")
        elem.click()
        
        number_of_images = self.config['image_numbers'] - self.downloaded
        self.sub = set()
        old_sub_len = 0
        same_len = 0 # check if there is no more new images
        while len(self.sub) <= number_of_images and same_len <8 :
            self.browser.execute_script("scrollBy(0,"+ str(self.scroll) +");")
            self.scroll += 950
            time.sleep(1)
            elem1 = self.browser.find_element_by_id("islmp")
            self.sub.update(elem1.find_elements_by_tag_name("img"))
            if(len(self.sub)==old_sub_len):
                same_len +=1
            else :
                old_sub_len = len(self.sub)
                same_len = 0
            print(str(len(self.sub))+'---- ' + str(same_len))
            try:
                show_more = self.browser.find_element_by_css_selector('input.mye4qd')
                show_more.click()
            except:
                pass

        self.download()
    def check_duplicate(self,image): # return if the image is already downloaded
        if str(image[:4]) != "http":
            h = Duplicate().dhash(image)
        else :
            h = image
        if h in self.hashes :
            self.removed +=1
            return True 
        else :
            self.hashes.add(h)
            return False 

    def readb64(self,src):
        try :
            base64_string = src.split(',')[1]
            sbuf = BytesIO()
            sbuf.write(base64.b64decode(base64_string))
            pimg = Image.open(sbuf)
            return np.array(pimg)
        except:
            return src
    def download(self):
        try:
            os.mkdir(self.config['download_folder'][0])
        except FileExistsError:
            pass

        error = 0
        for i in tqdm(self.sub):
            src = i.get_attribute('src')
            try:
                if src != None and src!='':
                    src  = str(src)
                    if not self.check_duplicate(self.readb64(src)):
                        self.downloaded+=1
                        urllib.request.urlretrieve(src, os.path.join(self.config['download_folder'][0],'image'+str(self.downloaded)+'.jpg'))
                else:
                    raise TypeError
            except :
                error += 1
        print('Total_download : {} , Total_removed : {} , errors {}'.format(self.downloaded,self.removed,error))
        if (self.downloaded) < self.config['image_numbers']:
            self.search_engine_index+=1
            print('Switching to {} engine ...'.format(self.search_engine[self.search_engine_index]))
            self.crowl()