from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm.auto import tqdm
import pandas as pd
import re

options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
options.add_argument('start-maximized')
driver = webdriver.Chrome(r'C:\Users\imsan\chromedriver.exe', options=options)


# get base url & log-in

base = 'https://~~'

ID = 'yourID'
PW = 'yourPW'

driver.get(base)
driver.implicitly_wait(1)

driver.find_element_by_id('user-email').send_keys(ID)
driver.find_element_by_id('user-password').send_keys(PW)

# log-in button
driver.find_element_by_xpath('//*[@id="main"]/div/section/div/div/div/form/div[2]/button').click()
driver.implicitly_wait(1)


# go to class

driver.find_element_by_class_name('fcb2e-curation-list-item__title').click()
driver.implicitly_wait(3)

try:
    driver.find_element_by_xpath('//aside[@class="classroom-modal classroom-dialog"]/*[name()="nav"]/*[name()="svg"][@aria-label="닫기"]').click()
    driver.implicitly_wait(1)
except:
    pass


# assume all arrows are pointing downward

narrow_arrow_class = 'fc-accordion-menu__header__arrow-icon'
for narrow_arrow in list(filter(lambda x: x.get_attribute('class')==narrow_arrow_class, 
                     driver.find_elements_by_tag_name('div'))):
    narrow_arrow.click()
    
    
spans = driver.find_elements_by_tag_name('span')
lectures = list(
    filter(lambda x: x.get_attribute('class') in 
           ['classroom-sidebar-clip__chapter__clip__title', 
            'classroom-sidebar-clip__chapter__clip__title classroom-sidebar-clip__chapter__clip__title--active'], 
           spans))



SAVE_PATH = 'C:/Users/imsan/Desktop/FC_GAN_TEMP/'
for lecture in tqdm(lectures):
    SAVE_PATH_file = SAVE_PATH+lecture.text+'.mp4'
    
    lecture.click()
    driver.implicitly_wait(3)

    try:
        driver.find_element_by_xpath('//aside[@class="classroom-modal classroom-dialog"]/*[name()="nav"]/*[name()="svg"][@aria-label="닫기"]').click()
        driver.implicitly_wait(1)
    except:
        pass
    
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
    url = driver.find_element_by_xpath('//*[@id="kollus_player_html5_api"]').get_attribute('src')

    request.urlretrieve(url, SAVE_PATH_file)

    driver.switch_to.default_content()
    driver.implicitly_wait(3)
