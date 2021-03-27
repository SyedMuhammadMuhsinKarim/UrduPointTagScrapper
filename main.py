from parallel_requests import ParallelRequests
from gzip_to_xml import gzip_to_xml

url = 'https://www.urdupoint.com/sitemap/daily/data/2021/2021-03-15.xml.gz'
content = gzip_to_xml(url)
print(content)