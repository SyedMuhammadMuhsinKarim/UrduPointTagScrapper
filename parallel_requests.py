import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs

class ParallelRequests:
  def __init__(self, urls, pars = 'html.parser'):
    self.urls = urls
    self.pars = pars

  async def __fetch(self, url, session):
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