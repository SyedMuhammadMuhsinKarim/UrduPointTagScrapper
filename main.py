import pandas as pd
from pandas import DataFrame
import datetime
from pymongo import MongoClient
import dns

from parallel_requests import calling_event
from gzip_to_xml import gzip_to_xml
from get_elements import Get_Elements
from link_cleaner import post_link_cleaning
from time_extaractors import post_time_extraction
# from dirctory import check_dir

pd.set_option("display.max_columns", 100)

dd = "02" #datetime.datetime.now().strftime('%d')
yyyy = datetime.datetime.now().strftime('%Y')
mm = datetime.datetime.now().strftime('%m')

url = f'https://www.urdupoint.com/sitemap/daily/data/{yyyy}/{yyyy}-{mm}-{dd}.xml.gz'
content_xml = gzip_to_xml(url)
news_links = post_link_cleaning(content_xml)
content_posts = calling_event(news_links)
headlines=Get_Elements(content_posts).get_headlines()
categories,categories_links = Get_Elements(content_posts).get_category()

def df_to_json(yyyy, mm, dd):
  with open(f'NewsData/{yyyy}/{mm}/{yyyy}-{mm}-{dd}.json', 'w', encoding='utf-8-sig') as file:
    df.to_json(file, force_ascii=False)

try: 
  news_time = post_time_extraction(content_posts)
  df = DataFrame([headlines, categories, news_time], index=['headlines', 'categories', 'time']).T
except:
  df = DataFrame([headlines, categories], index=['headlines', 'categories',]).T
  df['time'] = datetime.date(int(yyyy), int(mm), int(dd)).isoformat()

client =  MongoClient("mongodb+srv://demo:zRH4JBa8ED7nDSnE@cluster0.al9iw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['newses']
collection = db['news_datasets']
df.reset_index(inplace=True)
data_dict = df.to_dict("records")
collection.insert_many(data_dict)