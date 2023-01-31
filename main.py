import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

s = Service("C:/Users/shree/Desktop/chromedriver.exe") #webdriver path

options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)

#To open chrome automatically
driver = webdriver.Chrome(service = s, options = options)

#to search CarTrade link on chrome
driver.get("https://www.cartrade.com/buy-used-cars/mumbai/c/#so=-1&sc=-1&city=1")
#collect html from page
html = driver.page_source
soup = BeautifulSoup(html, features="html.parser")

img = []
name = []
price = []
kms_driven = []
fuel_type = []
emi = []
actual_pr = []
count = 1

#while loop to load first two page
while True:

    #Iterate over each item
    for i in soup.find_all('li', class_="blk_grid_new"): #li containd information about each item

        img.append(i.find_all('img', class_="overflow-hidden")[0].get('src')) #extract image
        name.append(i.find('h2').text.strip())#extract name
        price.append(i.find('div', class_='cr_prc').text.replace('Make', '').replace('Offer', '')[:20].strip()) #extract price
        kms_driven.append(i.find('div', class_='info_cr_new').find('ul').find_all('li')[0].text) #extract km driven
        fuel_type.append(i.find('div', class_='info_cr_new').find('ul').find_all('li')[2].text) #extract fuel type
        actual_pr.append(i.find('div', class_='cr_prc').find_all('span')[1].text.replace('Offer', '').strip().replace('Make', '')) #extract actual price

        #extract emi.we will use try and except to replace absent value with nan
        try:
            emi.append(i.find('span', class_='pull-left').text)
        except:
            emi.append(np.nan)

    time.sleep(2)
    #click on a next
    link = driver.find_element(by=By.XPATH, value='//*[@id="buypage2"]/div/ul/li[4]/a')
    link.click()

    count+=1
    print(f'done{count}')
    if count ==3:
        break

#while loop to load page from 2 onwords
while True:
    #try and except to stop while loop at end of the page.
    try:
        for i in soup.find_all('li', class_="blk_grid_new"):
            img.append(i.find_all('img', class_="overflow-hidden")[0].get('src'))
            name.append(i.find('h2').text.strip())
            price.append(i.find('div', class_='cr_prc').text.replace('Make', '').replace('Offer', '')[:20].strip())
            kms_driven.append(i.find('div', class_='info_cr_new').find('ul').find_all('li')[0].text)
            fuel_type.append(i.find('div', class_='info_cr_new').find('ul').find_all('li')[2].text)
            actual_pr.append(i.find('div', class_='cr_prc').find_all('span')[1].text.replace('Offer', '').strip().replace('Make', ''))

            try:
                emi.append(i.find('span', class_='pull-left').text)
            except:
                emi.append(np.nan)

        time.sleep(2)
        driver.find_element(by = By.XPATH, value = '//*[@id="buypage2"]/div/ul/li[7]/a').click()


        count+= 1
        print(f'done{count}')
        #if count ==150:
        #    break
    except:
        break
n = pd.DataFrame({'img':img,'name':name, 'price':price, 'emi' : emi, 'kms_driven':kms_driven, 'fuel_type':fuel_type, 'actual_pr':actual_pr})
print(n)

n.to_csv('car1.csv')