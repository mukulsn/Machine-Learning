#%%
# THIS SCRIPT IS TO DIRECTLY GET API DATA FROM AJIO
# DATE = 17 MARCH 2024
#%%
import pandas as pd
import time
# %%
# import requests module 
import requests 

# Making a get request 
response = requests.get('https://www.ajio.com/api/category/830303011?fields=SITE&currentPage=1&pageSize=100&format=json&query=%3Arelevance%3Abrand%3ASHOWOFF&sortBy=relevance&gridColumns=5&facets=brand%3ASHOWOFF&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true') 

# Store JSON data in API_Data 
API_Data = response.json() 

# # Print json data using loop 
# for key in API_Data:{ 
# 	print(key,":", API_Data[key]) 
# }

# %%
df = pd.DataFrame()
# main_data = pd.DataFrame()
counter = 0
for j in range(15,20,1):
    url = f"https://www.ajio.com/api/category/830303011?fields=SITE&currentPage={j+1}&pageSize=100&format=json&query=%3Arelevance%3Abrand%3ASHOWOFF&sortBy=relevance&gridColumns=5&facets=brand%3ASHOWOFF&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true"
    response = requests.get(url) 
    API_Data = response.json() 
    
    for index,i in enumerate(API_Data['products']):
        abc = i
        # print(i)
        # break
        df.loc[index,'PID'] = i['fnlColorVariantData']['colorGroup']
        df.loc[index,'product_image_url'] = i['fnlColorVariantData']['outfitPictureURL']
        df.loc[index,'brand'] = i['fnlColorVariantData']['brandName']
        try:
            df.loc[index,'rating'] = i['averageRating']
        except:
            df.loc[index,'rating'] = None
        df.loc[index,'dp'] = i['price']['value']
        df.loc[index,'sp'] = i['wasPriceData']['value']
        df.loc[index,'product'] = i['name']
        df.loc[index,'Link'] = 'https://www.ajio.com' + i['url']
        df.loc[index,'offer price'] = i['offerPrice']['value']
        try:
            df['number of ratings'] = i['ratingCount']
        except:
            df['number of ratings'] = None
        # print(df)
        counter+=1
    print(f'page completed {j+1}')
    main_data = pd.concat([main_data,df])
    if j % 2 == 0:
        time.sleep(5)
    else:
        time.sleep(5)

df
# %%
main_data.to_csv('final_data_ajio_showoff.csv')
# %%
