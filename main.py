import pandas as pd
from pandas import DataFrame
import datetime
from pymongo import MongoClient
import dns
from pymongo.write_concern import WriteConcern
from parallel_requests import calling_event
from gzip_to_xml import gzip_to_xml
from get_elements import Get_Elements
from link_cleaner import post_link_cleaning
from time_extaractors import post_time_extraction
# from dirctory import check_dir
import os

def df_to_json(yyyy, mm, dd):
    with open(f'NewsData/{yyyy}/{mm}/{yyyy}-{mm}-{dd}.json', 'w', encoding='utf-8-sig') as file:
        df.to_json(file, force_ascii=False)

def writing_db(df):
    try:
        print("DB WRITING")
        client =  MongoClient(db)
        db = client['newses']
        collection = db['news_datasets']
        df.reset_index(inplace=True)
        data_dict = df.to_dict("records")
        collection.with_options(write_concern=WriteConcern(w=0)).insert_many(data_dict, ordered=False)
    except Exception as e:
        raise e

db = os.getenv("DB")
pd.set_option("display.max_columns", 100)

month_days = { 1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31, 4: 30, 6: 30, 9: 30, 11: 30, 2: 28 }
months = 12
yyyy = datetime.datetime.now().strftime('%Y')

urls = []
for j in range(1, months + 1):
    range_month = month_days[j]
    for i in range(1, range_month + 1):
        if datetime .datetime(int(yyyy), j, i).date() < datetime.datetime.now().date():
            dd = f"{str(i)}" if len(str(i)) > 1 else f"0{str(i)}"
            mm = f"{str(j)}" if len(str(j)) > 1 else f"0{str(j)}"
            urls.append(f'https://www.urdupoint.com/sitemap/daily/data/{yyyy}/{yyyy}-{mm}-{dd}.xml.gz')
    
for url in urls[:10]:
    try: 
        content_xml = gzip_to_xml(url)
    except Exception as e:
        print(e)
        continue
    
    news_links = post_link_cleaning(content_xml)
    content_posts = calling_event(news_links)

    with open("content.txt", "w") as f:
        f.write(str(content_posts))
        break
    
    headlines = Get_Elements(content_posts).get_headlines()
    categories,categories_links = Get_Elements(content_posts).get_category()
    try: 
        news_time = post_time_extraction(content_posts)
        df = DataFrame([headlines, categories, news_time, url], index=['headlines', 'categories', 'time']).T
    except:
        df = DataFrame([headlines, categories, url], index=['headlines', 'categories',]).T
        df['time'] = datetime.date(int(yyyy), int(mm), int(dd)).isoformat()

