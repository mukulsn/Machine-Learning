# This is working file for myntra
# scope of scraping is it will scrape the pages given that the pages number should be given in for loop. this file is working fine and do not need code correction

#MAIN CODE ----

#%%

print('hello')
#%%
import urllib.request
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re
import os

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
driver=webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless=new')
# chrome_options.add_argument('--disable-dev-shm-usage')

# ######### very important line for headless webdriver  --> source https://stackoverflow.com/questions/62684000/selenium-with-headless-chromedriver-not-able-to-scrape-web-data
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# chrome_options.add_argument(f'user-agent={user_agent}')
# ######################
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)


# driver.get('https://www.myntra.com/')

#%%

def scroll_till_end(driver):

    # Scroll the page gradually
    scroll_speed = 60 # Adjust scroll speed as needed (milliseconds) 
    scroll_pause_time = 0.1 # Adjust pause time as needed (seconds)
    current_scroll_position = 0

    page_height = driver.execute_script("return document.body.scrollHeight")
    print(f'page height {page_height}')

    while current_scroll_position < page_height:
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        current_scroll_position += scroll_speed
        time.sleep(scroll_pause_time)
        page_height = driver.execute_script("return document.body.scrollHeight")
        print(f'page height {page_height}')

def absolute_number(num):
    a = str(num)
    if a.find('k') == -1:
        return a
    elif a.find('k') != 1:
        return int(float(a[:-1]) * 1000)

def extract_pid(text,pattern):
    return text.rfind(pattern,0,text.rfind(pattern))

def page_number_extract(page):
    var = None
    page_number = page.find('=')
    if page_number == -1:
        var = 1
    else:
        var = page[page_number+1:]
    return var

def working_data(soup):
    bigbox = soup.findAll("li",{"class":"product-base"})
    prod_meta_info = soup.findAll("div",{"class":"product-productMetaInfo"})
    prod_rating = soup.findAll("div",{"class":"product-ratingsContainerproduct-ratingsContainer"})
    prod_image = soup.findAll("div",{"class":"product-imageSliderContainer"})
    pagination_number =soup.findAll("ul",{"class":"pagination-container"})
    #new_season = soup.findAll('div',{'class':'xcelerator-plpxceleratorImageTag'})

# new_season = soup.findAll('div',{'class':'results-showMoreContainer'})

    href = []
    brand = []
    product = []
    prod_dp =[]
    prod_sp = []
    prod_discp = []
    prod_rating = []
    prod_ratingc = []
    prod_img = []
    page_number = []
    season_tag = []
    few_left = []
    total_items = []
    pid_list = []
    prod_ratingc_abs = []
    pp_price = []

    for i in range(len(bigbox)): # add iferror in the code
        print(i)
        link= "https://www.myntra.com/"+bigbox[i].a['href']
        pid = link[extract_pid(link,'/'):]
        pid = pid[1:pid.rfind('/')]
        title_brand = prod_meta_info[i].h3.text
        title_product = prod_meta_info[i].h4.text
        try:
            pp = prod_meta_info[i].find("div",{'class':'product-price'}).text
        except:
            pp = None
        try:
            dp = prod_meta_info[i].find("span",{'class':'product-discountedPrice'}).text
            # print(f'dp is {dp}')
        except:
            dp= None
        try:
            sp = prod_meta_info[i].find("span",{'class':'product-strike'}).text
        except:
            sp = None
        try:
            product_discount_percentage = prod_meta_info[i].find("span", {'class':'product-discountPercentage'}).text   
        except:
            product_discount_percentage =None
        try:
            product_rating = bigbox[i].findAll("div",{"class":"product-ratingsContainer"})[0].span.text
        except:
            product_rating = None
        try:
            product_rating_count = bigbox[i].findAll("div",{"class":"product-ratingsCount"})[0].text[1:]# product_rating_count = absolute_number(product_rating_count)
        except:
            product_rating_count = None
        try:
            product_rating_count_abs = absolute_number(product_rating_count)
        except:
            product_rating_count_abs = None
        try:
            product_image = prod_image[i].div.div.picture.img['src']
        except:
            product_image = None
        try:
            pg_number = pagination_number[0].findAll('li',{'class':'pagination-active'})[0].a['href']
            pg_number = page_number_extract(pg_number)
        except:
            pg_number = None
        try:
            season_tag_var = prod_image[i].div.find("div",{'class':'xcelerator-plpXceleratorImageTag'}).text
        except:
            season_tag_var = None
        try:
            few_left_var = prod_meta_info[i].find('div',{'class':'xcelerator-plpXceleratorInfoTag'}).text
        except:
            few_left_var = None
        try:
            total_itms = soup.findAll('div', {'class':'title-container'})[0].span.text
        except:
            total_itms = None

        href.append(link)
        brand.append(title_brand)
        product.append(title_product)
        prod_dp.append(dp)
        prod_sp.append(sp)
        prod_discp.append(product_discount_percentage)
        prod_rating.append(product_rating)
        prod_ratingc.append(product_rating_count)
        prod_img.append(product_image)
        page_number.append(pg_number)
        season_tag.append(season_tag_var)
        few_left.append(few_left_var)
        total_items.append(total_itms)
        prod_ratingc_abs.append(product_rating_count_abs)
        pid_list.append(pid)
        pp_price.append(pp)

    df =pd.DataFrame({'Brand':brand,
                        'Link':href,
                        'PID':pid_list,
                        'Product':product,
                        'product_price':pp_price,
                        'Dp':prod_dp,
                        'Sp':prod_sp,
                        'Product_discount_percentage':prod_discp,
                        'Product_rating':prod_rating,
                        'prod_rating_count':prod_ratingc,
                        'prod_rating_count_abs':prod_ratingc_abs,
                        'product_image_url':prod_img,
                        'page number':page_number,
                        'season_tag':season_tag,
                        'only_few_left':few_left,
                        'total_items':total_items})

    # #adding product rating count absolute numbers# df['product_rating_count_abs'] = absolute_number(product_rating_count)PTD# df['PID'] = pid[1:pid.rfind('/')]

    return df


# %%

main_data = pd.DataFrame()
for i in range(26): # because 20 dresses have 2663 on myntra
    if i == 0:
        driver.get('httphttps://www.myntra.com/dress-material')    
    else:
        driver.get(f'https://www.myntra.com/dress-material&p={i+1}')
    print('page loaded')
    scroll_till_end(driver)
    print('scroll completed')
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    df = working_data(soup)
    main_data=pd.concat([main_data,df])
    # break
# driver.close()
main_data.to_csv(r'data\myntra dress material.csv')

# %%
