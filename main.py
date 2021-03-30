import time
from pandas import DataFrame
from parallel_requests import calling_event
from gzip_to_xml import gzip_to_xml
from get_elements import Get_Elements
from link_cleaner import post_link_cleaning
from time_extaractors import post_time_extraction
from dirctory import check_dir

dd = "28"
yyyy = "2021"
mm = "02"

# Variables
url = f'https://www.urdupoint.com/sitemap/daily/data/{yyyy}/{yyyy}-{mm}-{dd}.xml.gz'
start_event = time.time() # For Debbugg

# Open gZip content and get XML content
content_xml = gzip_to_xml(url)
news_links = post_link_cleaning(content_xml)

# Get Contents by aSyncIO
start = time.time()  # For Debbugg
content_posts = calling_event(news_links)
print(f"aSyncIo\nTime Elapsed: {time.time()-start} seconds, \
    \n requests per second: {news_links.shape[0]//int(time.time()-start)}")

# Get Headlines/Title of the posts
headlines=Get_Elements(content_posts).get_headlines()
categories,categories_links = Get_Elements(content_posts).get_category()

# Get Times of the posts
try: 
  news_time = post_time_extraction(content_posts)
  df = DataFrame([headlines, categories, news_time], index=['headlines', 'categories', 'time']).T
  print(df) # For Debbugg
except:
  df = DataFrame([headlines, categories], index=['headlines', 'categories',]).T
  print(df) # For Debbugg

check_dir(yyyy, mm)

df.to_csv(f'NewsData/{yyyy}/{mm}/{yyyy}-{mm}-{dd}.csv', encoding='utf-8-sig')

print(time.time() - start_event) # For Debbugg