from pandas import Series
import numpy as np

def post_link_cleaning(links_data):
    news_links = Series([
        elem.text for elem in links_data
    ]).apply(lambda x: x if x.split("/")[4] == 'livenews' else np.nan)
    return news_links.loc[~news_links.isnull()]
