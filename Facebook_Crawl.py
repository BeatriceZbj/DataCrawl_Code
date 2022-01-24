import csv
from getpass import getpass
from time import sleep
from numpy.lib.type_check import nan_to_num
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import requests
import json
import time


driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\chromedriver.exe')
driver.get('https://www.facebook.com')
username = driver.find_element_by_xpath('//input[@id="email"]')
username.send_keys('beatrice77.zheng@gmail.com')
my_password = 'Zbj19950412@'
password = driver.find_element_by_xpath('//input[@id="pass"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)
dictCookies = driver.get_cookies()
jsonCookies = json.dumps(dictCookies) 
with open("cookies_fb.json", "w") as fp:
    fp.write(jsonCookies)


driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\chromedriver.exe')
driver.get('https://www.facebook.com')
sleep(1)
driver.delete_all_cookies() 
with open('cookies_fb.json', 'r', encoding='utf-8') as f:
    listCookies = json.loads(f.read())  

for cookie in listCookies:
    driver.add_cookie({ 
        'domain': cookie['domain'],
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/'
    })
driver.get('https://www.facebook.com/ChinaGlobalTVNetwork')




content = []
for _ in range(1000):
    
    patterns = driver.find_elements_by_xpath('//div[@class = "k4urcfbm dp1hu0rb d2edcug0 cbu4d94t j83agx80 bp9cbjyn"]/div/div')
    last_label_tweet = None
    for pat in patterns:
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        try:
            try:
                post_links = pat.find_element_by_xpath('.//div[@class = "l9j0dhe7"]/div/div/div/div/a').get_attribute('href')
            except NoSuchElementException:
                post_links = '-'
            try:
                text = pat.find_element_by_xpath('.//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh oo9gr5id hzawbc8m"]').text
            except:
                pass

            try:
                likes = pat.find_element_by_xpath('.//span[@class="pcp91wgn"]').text
            except:
                pass

            try:
                comments = pat.find_element_by_xpath('.//div[@class="gtad4xkn"][1]').text
            except:
                pass

            try:
                shares = pat.find_element_by_xpath('.//div[@class="gtad4xkn"][2]/span/div/span').text
            except:
                pass

            try:
                video = pat.find_element_by_xpath('.//video[@class = "k4urcfbm datstx6m a8c37x1j"]').get_attribute('src')
            except NoSuchElementException:
                video = '-'

            time_ = pat.find_element_by_xpath('.//div[@class="qzhwtbm6 knvmm38d"][2]/span/span/span[3]/span/a/span').text
            if "分钟" in time_:
                time = time_
            else:
                time = pat.find_element_by_xpath('.//div[@class="qzhwtbm6 knvmm38d"][2]/span/span/span[3]/span/a/span').text



            comments_sum = {}
            try:

                comments_people = pat.find_elements_by_xpath('.//div[@class = "cwj9ozl2 tvmbv18p"]/ul/li')

                for item in comments_people:
                    comment_user = item.find_element_by_xpath('.//div/div/div[2]/div/div/div/div/div/div/span').text
                    comment_text = item.find_element_by_xpath('.//div/div/div[2]/div/div/div/div/div/div/div').text
                    comments_sum[comment_user] = comment_text
            except:
                pass
            try:
                pat.find_element_by_xpath('.//span[@class = "j83agx80 fv0vnmcu hpfvmrgz"]').click()


                comments_people = pat.find_elements_by_xpath('.//div[@class = "cwj9ozl2 tvmbv18p"]/ul/li')

                for item in comments_people:
                    comment_user = item.find_element_by_xpath('.//div/div/div[2]/div/div/div/div/div/div/span').text
                    comment_text = item.find_element_by_xpath('.//div/div/div[2]/div/div/div/div/div/div/div').text
                    comments_sum[comment_user] = comment_text
            except:
                pass

            try:
                comments_people = pat.find_elements_by_xpath('.//div[@class = "cwj9ozl2 tvmbv18p"]/div[4]/div/div')
                for item in comments_people:
                    comment_user = item.find_element_by_xpath('.//div/div[2]/div/div/div/div/div/div/span/a/span/span').text
                    comment_text = item.find_element_by_xpath('.//div/div[2]/div/div/div/div/div/div/div/span').text
                    comments_sum[comment_user] = comment_text
            except:
                pass
        except:
            pass
        
        try:

            last_label_tweet = pat
            if last_label_tweet is not None:
                driver.execute_script("arguments[0].scrollIntoView();", last_label_tweet)
                sleep(5)
            else:
                break
        except:
            pass

        FB_content = (post_links ,text, likes, comments, shares, video, time, comments_sum)
        content.append(FB_content)
        print(FB_content)
        
        with open('fb.csv','w', newline = '', encoding = 'utf-8-sig') as f:
            header = ['post_links', 'text', 'likes', 'comments', 'shares', 'video', 'time','comments_sum']            
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(content)
            