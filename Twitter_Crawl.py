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




browser = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\chromedriver.exe')
browser.get('https://twitter.com/search?q=China%20(from%3ABBCWorld)%20until%3A2021-07-31%20since%3A2021-06-30&src=typed_query&f=live')
sleep(2)



item_list = []
label_outer = browser.find_element_by_css_selector("main > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > section > div > div")
browser.execute_script("arguments[0].id = 'outer';", label_outer)  # 设置标题外层标签的ID
tweet_id_set = set()
n = 1

for _ in range(1000):
    last_label_tweet = None
    for label_tweet in label_outer.find_elements_by_xpath('//div[@data-testid="tweet"]'):  # 定位到推文标签
        item = {}
        

        if label := label_tweet.find_element_by_css_selector(
                "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > a"):
            
            if pattern := re.search("[0-9]+$", label.get_attribute("href")):
                item["tweet_id"] = pattern.group()
        
        if "tweet_id" not in item:
            browser.log("账号名称:" + user_name + "|未找到推文ID标签(第" + str(len(item_list)) + "条推文)")
            continue

 
        if item["tweet_id"] in tweet_id_set:
            continue

        tweet_id_set.add(item["tweet_id"])
        last_label_tweet = label_tweet


        if label := label_tweet.find_element_by_css_selector(
                "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > a > time"):
            item["time"] = label.get_attribute("datetime").replace("T", " ").replace(".000Z", "")


        if label := label_tweet.find_element_by_xpath(".//div[2]/div[2]/div[position()<3]"):
            item["text"] = label.text
    

#         if label := label_tweet.find_element_by_css_selector(
#                 "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div > div > div > div > div > a > div > div:nth-child(2) > div"):
#             item["author"] = label.text


        if label := label_tweet.find_element_by_xpath('.//div[2]/div/div/div/div[1]/a'):
            item["contentlinks"] = label.get_attribute('href')
            

        try:
            links = label_tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]/div/div/div/div[2]/a')
            item['articlelinks'] = links.get_attribute('href')
            print(links.get_attribute('href'))
        except:
            links = label_tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]//video')
            item['articlelinks'] = links.get_attribute('src')
        else:
             item['articlelinks'] = '-'
            
            
            
            



        if label := label_tweet.find_element_by_xpath(".//div[2]/div[2]/div[position()=3]/div"):
            if text := label.get_attribute("aria-label"):
                print(text)

                for feedback_item in text.split(","):
                    if "replies" in feedback_item:
                        if pattern := re.search("[0-9]+", feedback_item):
                            item["replies_"] = int(pattern.group())
                            print(int(pattern.group()))
                    if "Retweets" in feedback_item:
                        if pattern := re.search("[0-9]+", feedback_item):
                            item["retweets_"] = int(pattern.group())
                            print(int(pattern.group()))
                    if "likes" in feedback_item:
                        if pattern := re.search("[0-9]+", feedback_item):
                                item["likes_"] = int(pattern.group())
                                print(int(pattern.group()))

        item_list.append(item)


        

    if last_label_tweet is not None:
        browser.execute_script(.execute_script("arguments[0].scrollIntoView();", last_label_tweet)  # 滑动到推文标签
        time.sleep(3)
    else:
        break
        
    data = pd.DataFrame(item_list)
    data.to_excel('BBC_China.xlsx')