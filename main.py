# Official Modules
from bs4 import BeautifulSoup as bs
import lxml
import asyncio
import json
import time
import re
from pandas import DataFrame

# My Modules
from parallel_requests import ParallelRequests
from gzip_to_xml import gzip_to_xml
from get_elements import Get_Elements
from link_cleaner import post_link_cleaning

dd = "08"
yyyy = "2021"
mm = "03"

# Variables
url = f'https://www.urdupoint.com/sitemap/daily/data/{yyyy}/{yyyy}-{mm}-{dd}.xml.gz'
start_event = time.time() # For Debbugg

# Open gZip content and get XML content
content_xml = gzip_to_xml(url)

# Links Cleanings
news_links = post_link_cleaning(content_xml)

# Get Contents by aSyncIO
start = time.time()  # For Debbugg
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(ParallelRequests(news_links.to_list()).run())
content_posts = loop.run_until_complete(future)
end = time.time()  # For Debbugg
print(f"aSyncIo\nTime Elapsed: {end-start} seconds, \
    \n requests per second: {news_links.shape[0]//int(end-start)}")

# Get Headlines/Title of the posts
headlines=Get_Elements(content_posts).get_headlines()
categories,categories_links = Get_Elements(content_posts).get_category()

# Get Times of the posts
try: 
  timefinder_reg = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}")
  news_time = [re.findall(timefinder_reg, json.dumps(elem.find_all("script", attrs={'type': 'application/ld+json'})[3].contents))[0] for elem in content_posts]
  df = DataFrame([headlines, categories, news_time], index=['headlines', 'categories', 'time']).T
  print(df) # For Debbugg
except Exception as e:
  print(e) # For Debbugg
  df = DataFrame([headlines, categories], index=['headlines', 'categories',]).T
  print(df) # For Debbugg

print(url.split("/")[7].split(".")[0].split("-")) # For Debbugg
df.to_csv(f'NewsData/{2021}/{mm}/{yyyy}-{mm}-{dd}.csv', encoding='utf-8-sig')

end_event = time.time() # For Debbugg
print(end_event - start_event) # For Debbugg