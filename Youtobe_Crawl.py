from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import re
import time
import pandas as pd
from time import sleep
from selenium.webdriver.common.keys import Keys
import json
import csv
from selenium.webdriver.common.action_chains import ActionChains



driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\chromedriver.exe')
driver.get('https://www.youtube.com/c/cgtn/videos')
sleep(2)
# patterns = driver.find_elements_by_xpath('//div[@id="contents"]//ytd-grid-video-renderer')
# driver.execute_script("arguments[0].id = 'outer';", patterns)

# 最外层设置的遍历的意图其实是为了不断的下拉刷新，数字设定没有要求。一旦无法下拉刷新会触动break跳出循环
for _ in range(1000):
    # 设置一个当前的定位值
    last_label = None
    item_list = [] 
    # 每一次刷新都重新定位一下patterns，会赋给last_label一个新的pattern
    patterns = driver.find_elements_by_xpath('//div[@id="contents"]//ytd-grid-video-renderer')
    for pattern in patterns:
        video_links = pattern.find_element_by_xpath('.//h3/a').get_attribute('href')
        text = pattern.find_element_by_xpath('.//h3/a').text
        views = pattern.find_element_by_xpath('.//div[@id="metadata-container"]//span[1]').text
        time = pattern.find_element_by_xpath('.//div[@id="metadata-container"]//span[2]').text
        last_label = pattern
        youtobe = (time, text, views, video_links)
        item_list.append(youtobe)
    # 如果last_label是空值了，那么就不再继续下拉，跳出循环
    if last_label is not None:
            driver.execute_script("arguments[0].scrollIntoView();", last_label) 
            sleep(2)
    else:
        break
    print(item_list)
    
    #写入文件
    with open('cngt_youtobe.csv','w', newline = '', encoding = 'utf-8-sig') as f:
        header = ['time', 'text', 'views', 'video_links']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(item_list)


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\chromedriver.exe')
html = pd.read_excel('C:/Users/39118/Desktop/Jupiter/html.xlsx')['links'].tolist()



for link in range(393,len(html)):
    item_list = []
    driver.get(html[link])

    sleep(3)
     
#     scroll_add_crowd_button = driver.find_element_by_xpath('//span[@class="view-count style-scope ytd-video-view-count-renderer"]')

#     driver.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)

    sleep(2)
    links = html[link]
    views_count = driver.find_element_by_xpath('//span[@class="view-count style-scope ytd-video-view-count-renderer"]').text
    likes = driver.find_element_by_xpath('(//div[@id="top-level-buttons-computed"]//ytd-toggle-button-renderer[1]//yt-formatted-string)[1]').get_attribute('aria-label')
    dislikes = driver.find_element_by_xpath('(//div[@id="top-level-buttons-computed"]//ytd-toggle-button-renderer[2]//yt-formatted-string)[1]').get_attribute('aria-label')
    time = driver.find_element_by_xpath('//div[@id="info-strings"]//yt-formatted-string[@class="style-scope ytd-video-primary-info-renderer"]').text
    # 滑动到某一个指定的位置
    scroll_add_crowd_button = driver.find_element_by_xpath('//span[@class="view-count style-scope ytd-video-view-count-renderer"]')

    driver.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)
    sleep(2.5)
    comments = driver.find_element_by_xpath('//yt-formatted-string[@class="count-text style-scope ytd-comments-header-renderer"]').text
    items = (links, time, views_count, likes, dislikes, comments)
    item_list.append(items)
    print(html[link])
    with open('cngt_youtobe_items_9.csv','a', newline = '', encoding = 'utf-8-sig') as f:
#         header = ['links', 'time', 'views_count', 'likes', 'dislikes', 'comments']
        writer = csv.writer(f)
        writer.writerows(item_list)

