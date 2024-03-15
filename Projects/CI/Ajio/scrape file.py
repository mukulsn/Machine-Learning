# this file is working file, only some image urls are missing but 80% of urls are available in the file

#MAIN CODE --

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
from datetime import datetime

# datetime object containing current date and time
start = datetime.now()

#options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)
#options.add_argument("--start-maximized")
#driver=webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')

######### very important line for headless webdriver  --> source https://stackoverflow.com/questions/62684000/selenium-with-headless-chromedriver-not-able-to-scrape-web-data
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
# # ######################
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)


# driver.get('https://www.myntra.com/')

#%%

def driver_click(xpath):
    element = driver.find_element(By.XPATH, xpath)
    # driver.execute_script('arguments[0].scrollIntoView();')
    driver.execute_script('window.scrollBy(0,-200);')
    element.click()


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
    # bigbox = soup.findAll("li",{"class":"product-base"})
    prod_meta_info = soup.findAll("div",{"class":"product-productMetaInfo"})
    prod_rating = soup.findAll("div",{"class":"product-ratingsContainerproduct-ratingsContainer"})
    prod_image = soup.findAll("div",{"class":"product-imageSliderContainer"})
    pagination_number =soup.findAll("ul",{"class":"pagination-container"})
    #new_season = soup.findAll('div',{'class':'xcelerator-plpxceleratorImageTag'})

    all_sku = soup.select('div[class="contentHolder"]') 
    all_image = soup.select('div[class= "imgHolder"]')

    pid_url =soup.select('div[class="item rilrtl-products-list__item item"]')


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
    offer_price=[]
    exclusive=[]

    for i in range(len(all_sku)): # add iferror in the code
        print(i)
        # link= "https://www.myntra.com/"+bigbox[i].a['href']
        # pid = link[extract_pid(link,'/'):]
        # pid = pid[1:pid.rfind('/')]
        image_holder = all_image[i]
        link = "https://www.ajio.com" + pid_url[i].a['href']
        try:
            pid = pid_url[i].a['href'].rsplit('/',1)[1]
        except:
            pid = None
        title_brand= all_sku[i].find('div',{'class': 'brand'}).text #
        title_product= all_sku[i].find('div', {'class':'nameCls'}).text #
        try:
            pp = prod_meta_info[i].find("div", {'class': 'product-price'}).text
        except:
            pp = None
        try:
            dp = all_sku[i].find('span', {'class':"price"}).text 
            dp = dp.replace(chr(8377),"").replace(',','')
        except:
            dp = None
        try:
            sp= all_sku[i].find('span', {'class':"orginal-price"}).text
            sp = sp.replace(chr(8377), "").replace(',','')
        except:
            sp = None
        try:
            of_p = all_sku[i].find('span',{'class': "offer-pricess"}).text
            of_p = of_p.replace(chr(8377),"").replace(',','').replace(' off','')
        except:
            of_p = None
        try:
            product_discount_percentage =all_sku[i].find('span', {'class':"discount"}).text
            product_discount_percentage = product_discount_percentage.replace('(','').replace(')','').replace(' off','')
        except:
            product_discount_percentage = None
        try:
            excl =all_image[i].find('div', {'class':'exclusive'}).text
        except:
            excl = None
        try:
            product_rating= all_sku[i].findAll("div", {"class":"product-ratingsContainer"})[0].span.text
        except:
            product_rating= None
        try:
            product_rating_count= all_sku[i].findAll("div", {"class":"product-ratingsCount"})[0].text[1:] #product_rating_count absolute_number(product_rating_count)
        except:
            product_rating_count =None
        try:
            product_rating_count_abs =absolute_number(product_rating_count)
        except:
            product_rating_count_abs = None
        try:
            product_image= image_holder.find('img',{'class':"rilrtl-lazy-img rilrtl-lazy-img-loaded"})["src"]
        except:
            product_image = None
        try:    
            pg_number = pagination_number[0].findAll('11', {'class': 'pagination-active'})[0].a["href"]
            pg_number=page_number_extract(pg_number)
        except:
            pg_number = None
        try:
            season_tag_var =prod_image[i].div.find("div", {"class":"xcelerator-plpXceleratorImageTag"}).text
        except:
            season_tag_var= None
        try:
            few_left_var= prod_meta_info[i].find('div', {'class':'xcelerator-plpXceleratorInfoTag'}).text
        except:
            few_left_var=None
        try:
            total_itms = soup.find('div',{'class':'filter-container'}).div.div.text
        except:
            total_itms=None



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
        offer_price.append(of_p)
        exclusive.append(excl)

    df =pd.DataFrame({'Brand':brand,
                        'Link':href,
                        'PID':pid_list,
                        'Product':product,
                        # 'product_price':pp_price,
                        'Dp':prod_dp,
                        'Sp':prod_sp,
                        'offer_price_AJIO':offer_price,
                        'Exclusive_AJIO':exclusive,
                        'Product_discount_percentage':prod_discp,
                        # 'Product_rating':prod_rating,
                        # 'prod_rating_count':prod_ratingc,
                        # 'prod_rating_count_abs':prod_ratingc_abs,
                        'product_image_url':prod_img,
                        # 'page number':page_number,
                        # 'season_tag':season_tag,
                        # 'only_few_left':few_left,
                        'total_items':total_items})

    # #adding product rating count absolute numbers# df['product_rating_count_abs'] = absolute_number(product_rating_count)PTD# df['PID'] = pid[1:pid.rfind('/')]

    return df


# Define a function to check if all images are loaded
def are_all_images_loaded():
    try:
        # Find all image elements on the page
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        
        # Check if all images are loaded
        for img in img_elements:
            if not img.get_attribute("complete"):
                return False
        return True
    except:
        return False

def scroll_till_end(driver):

    # Scroll the page gradually
    scroll_speed = 50 # Adjust scroll speed as needed (milliseconds) 
    scroll_pause_time = 0.1 # Adjust pause time as needed (seconds)
    current_scroll_position = 0

    page_height = driver.execute_script("return document.body.scrollHeight")
    print(f'page height {page_height}')

    while current_scroll_position < 300000:
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        current_scroll_position += scroll_speed
        time.sleep(scroll_pause_time)
        page_height = driver.execute_script("return document.body.scrollHeight")
        print(f'page height {page_height}')
        if page_height > 10000:
            scroll_speed = 40 # Adjust scroll speed as needed (milliseconds) 
            scroll_pause_time = 0.1 # Adjust pause time as needed (seconds)
            

        # ####### EXPERIMENTING WITH PAGE WAIT STRATEGY
        # # Check if all images are loaded
        # if are_all_images_loaded():
        #     print("Some images failed to load.")
        #     time.sleep(3)

        #     # now reverse scrolling for 3 times
        #     for i in range(3):
        #         # time.sleep(1)
        #         current_scroll_position -= scroll_speed
        #         driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        #         # time.sleep(scroll_pause_time)
        #     time.sleep(scroll_pause_time)
        # else:
        #     print("All images are loaded properly.")
# %%

main_data = pd.DataFrame()
for i in range(1): # because 20 dresses have 2663 on myntra
    driver.get('https://www.ajio.com/women-dress-material/c/830303004')  # dress material
    # driver.get('https://www.ajio.com/c/830303011')  # kurta sets women
    time.sleep(2)
    driver_click('//*[@id="products"]/div[2]/div/div[2]/div/div[2]')
    # if i == 0:
    #     driver.get('https://www.myntra.com/20dresses')    
    # else:
    #     driver.get(f'https://www.myntra.com/20dresses&p={i+1}')
    print('new script')
    print('page loaded')
    scroll_till_end(driver)
    print('scroll completed')
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    df = working_data(soup)
    main_data=pd.concat([main_data,df])
    print(main_data)
    main_data.to_csv(r'data ajio.csv')
    break
driver.close()
# main_data.to_csv(r'data\ajio data experiment.csv')

# %%
end = datetime.now()

print(f'start time {start} and end time {end}')
