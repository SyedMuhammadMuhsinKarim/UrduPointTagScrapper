import requests
import gzip
from bs4 import BeautifulSoup as bs
from io import BytesIO

def gzip_to_xml(link):
  r = requests.get(link ,stream=True)
  g=gzip.GzipFile(fileobj=BytesIO(r.content))
  content=g.read()
  return bs(content, 'lxml').find_all('loc')[2:]