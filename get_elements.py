from get_content import Get_Content
import numpy as np

class Get_Elements:
    def __init__(self, content_posts):
        self.content_posts = content_posts

    def get_headlines(self):
        headlines_tags = Get_Content(self.content_posts, 'h1', 'class',
                                     'fs24 lh48 urdu ar rtl').content()
        headlines = [
            headlines_tags[i].text if headlines_tags[i] != None else np.nan
            for i in range(len(headlines_tags))
        ]
        return headlines

    def get_category(self):
        category_tag = Get_Content(self.content_posts, 'div', 'class', 'tagcloud rtl ar urdu').content()
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
          
        return categories, categories_links
