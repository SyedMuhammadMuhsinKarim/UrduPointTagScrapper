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
from get_content import Get_Content
from parallel_requests import ParallelRequests
from gzip_to_xml import gzip_to_xml

# Variables
url = 'https://www.urdupoint.com/sitemap/daily/data/2021/2021-03-27.xml.gz'
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
content_posts = ParallelRequests(news_links.head(50).to_list()).run()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(content_posts)
content_posts = loop.run_until_complete(future)
end = time.time()
print(f"aSyncIo\nTime Elapsed: {end-start} seconds, \n \
    requests per second: {news_links.shape[0]//int(end-start)}")

# Get Headlines/Title of the posts
headlines_tags = Get_Content(content_posts, 'h1', 'class',
                             'fs24 lh48 urdu ar rtl').content()
headlines = [
    headlines_tags[i].text if headlines_tags[i] != None else np.nan
    for i in range(len(headlines_tags))
]

# Get Categories/Tags of the posts
category_tag = [
    elem.find('div', attrs={"class": "tagcloud rtl ar urdu"})
    for elem in content_posts
]
category = [
    category_tag[i].find_all('a') if category_tag[i] != None else []
    for i in range(len(category_tag))
]
categories = []
categories_links = []
for item in category:
    category_per_item = []
    category_link_per_item = []
    for elm in item:
        category_per_item.append(elm.text)
        category_link_per_item.append(elm.attrs['href'])
    categories.append(list(set(category_per_item)))
    categories_links.append(list(set(category_link_per_item)))


timefinder_reg = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}")
news_time = [re.findall(timefinder_reg, json.dumps(elem.find_all("script", attrs={'type': 'application/ld+json'})[3].contents))[0] for elem in content_posts]
df = DataFrame([headlines, categories, news_time], index=['headlines', 'categories', 'time']).T
print(df)

end_event = time.time()
print(end_event - start_event)
