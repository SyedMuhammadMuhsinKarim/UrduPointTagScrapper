import requests
import gzip

def gzip_to_xml(link):
  r = requests.get(link ,stream=True)
  g=gzip.GzipFile(fileobj=BytesIO(r.content))
  content=g.read()
  return content