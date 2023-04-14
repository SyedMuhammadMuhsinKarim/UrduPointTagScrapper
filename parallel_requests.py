import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs

class ParallelRequests:
  pars = 'html.parser'
  def __init__(self, urls):
    self.urls = urls

  async def __fetch(self, url, session):
    """
        1. The function takes in three arguments:
            - url: the url to be fetched
            - session: the session to be used to fetch the url
            - self.pars: the parameters to be passed to the function
        2. The function then uses the session to fetch the url.
        3. The function then reads the response from the url.
    """
    async with session.get(url) as response:
       resp = await response.read()
       return bs(resp, self.pars, from_encoding="utf-8")

  async def run(self):
    tasks = []
    async with ClientSession() as session:
      for url in self.urls:
        fetch_resp = self.__fetch(url, session)
        task = asyncio.ensure_future(fetch_resp)
        tasks.append(task)
      return await asyncio.gather(*tasks)

def calling_event(content):
  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(ParallelRequests(content.to_list()).run())
  return loop.run_until_complete(future)