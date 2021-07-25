from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

class Downloader():
    def __init__(self,config):
        self.config = config 
        
    def crowl(self):

        browser = webdriver.Chrome("Assets/chromedriver") #incase you are chrome
        browser.get("https://www.google.com/?hl=en")

        search = browser.find_element_by_name("q")
        search.send_keys(self.config['search_key'] , Keys.ENTER)
        elem = browser.find_element_by_link_text("Images")
        elem.get_attribute("href")
        elem.click()

        value = 0
        number_of_images = self.config['image_numbers']
        self.sub = []
        while len(self.sub) < number_of_images :
            browser.execute_script("scrollBy("+ str(value) +",+1000);")
            value += 1000
            time.sleep(2)
            print(len(self.sub))
            elem1 = browser.find_element_by_id("islmp")
            self.sub += elem1.find_elements_by_tag_name("img")
        if  len(self.sub) - number_of_images > 0 :
            self.sub = self.sub[:number_of_images - len(self.sub)]

        self.download()

    def download(self):
        try:
            os.mkdir(self.config['download_folder'][0])
        except FileExistsError:
            pass

        count = 0
        error = 0
        print(len(self.sub))
        for i in tqdm(range(len(self.sub))):
            src = self.sub[i].get_attribute('src')
            try:
                if src != None:
                    src  = str(src)
                    count+=1
                    urllib.request.urlretrieve(src, os.path.join(self.config['download_folder'][0],'image'+str(count)+'.jpg'))
                else:
                    raise TypeError
            except TypeError:
                error += 1
        print(error)
