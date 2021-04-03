# from pandas import DataFrame
# import datetime
# from parallel_requests import calling_event
# from gzip_to_xml import gzip_to_xml
# from get_elements import Get_Elements
# from link_cleaner import post_link_cleaning
# from time_extaractors import post_time_extraction
# from dirctory import check_dir

# dd = datetime.datetime.now().strftime('%d')
# yyyy = datetime.datetime.now().strftime('%Y')
# mm = datetime.datetime.now().strftime('%m')

# url = f'https://www.urdupoint.com/sitemap/daily/data/{yyyy}/{yyyy}-{mm}-{dd}.xml.gz'
# content_xml = gzip_to_xml(url)
# news_links = post_link_cleaning(content_xml)
# content_posts = calling_event(news_links)
# headlines=Get_Elements(content_posts).get_headlines()
# categories,categories_links = Get_Elements(content_posts).get_category()

# try: 
#   news_time = post_time_extraction(content_posts)
#   df = DataFrame([headlines, categories, news_time], index=['headlines', 'categories', 'time']).T
#   df.to_csv(f'NewsData/{yyyy}/{mm}/{yyyy}-{mm}-{dd}.csv', encoding='utf-8-sig')
# except:
#   df = DataFrame([headlines, categories], index=['headlines', 'categories',]).T
#   check_dir(yyyy, mm)
#   df.to_csv(f'NewsDataWithoutTime/{yyyy}/{mm}/{yyyy}-{mm}-{dd}.csv', encoding='utf-8-sig')

import os
import glob
import pandas as pd

pd.set_option("display.max_columns", 100)

if os.path.exists('NewsDataWithoutTime/2021/03'):
  all_filenames = [i for i in glob.glob('NewsData/2021/02/*.csv')]
  combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
  print(combined_csv)
