# Official Modules
from bs4 import BeautifulSoup as bs
import lxml
import asyncio
import json
import time
import numpy as np
import re
from pandas import Series, DataFrame

# My Modules
from parallel_requests import ParallelRequests
from gzip_to_xml import gzip_to_xml

dd = "18"
yyyy = "2021"
mm = "03"

# Variables
url = f'https://www.urdupoint.com/sitemap/daily/data/{yyyy}/{yyyy}-{mm}-{dd}.xml.gz'
start_event = time.time()
# Open gZip content and get XML content
content_xml = gzip_to_xml(url)
content_xml = bs(content_xml, 'lxml').find_all('loc')[2:]

# Links Cleanings
news_links = Series([elem.text for elem in content_xml])
news_links = news_links.apply(lambda x: x
                              if x.split("/")[4] == 'livenews' else np.nan)
news_links = news_links.loc[~news_links.isnull()]

# Get Contents by aSyncIO
start = time.time()
content_posts = ParallelRequests(news_links.to_list()).run()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(content_posts)
content_posts = loop.run_until_complete(future)
end = time.time()
print(f"aSyncIo\nTime Elapsed: {end-start} seconds, \n \
    requests per second: {news_links.shape[0]//int(end-start)}")

# Get Headlines/Title of the posts
from get_elements import Get_Elements
headlines=Get_Elements(content_posts).get_headlines()
categories,categories_links = Get_Elements(content_posts).get_category()

# Get Times of the posts
try: 
  timefinder_reg = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}")
  news_time = [re.findall(timefinder_reg, json.dumps(elem.find_all("script", attrs={'type': 'application/ld+json'})[3].contents))[0] for elem in content_posts]
  df = DataFrame([headlines, categories, news_time], index=['headlines', 'categories', 'time']).T
  print(df)
except Exception as e:
  print(e)
  # Get DataFrames
  df = DataFrame([headlines, categories], index=['headlines', 'categories',]).T
  print(df)

print(url.split("/")[7].split(".")[0].split("-"))
df.to_csv(f'NewsData/{2021}/Mar/{yyyy}-{mm}-{dd}.csv', encoding='utf-8-sig')

end_event = time.time()
print(end_event - start_event)