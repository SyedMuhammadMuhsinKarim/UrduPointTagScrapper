import re
import json

def post_time_extraction(content_posts):
    timefinder_reg = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}")
    return [re.findall(timefinder_reg, json.dumps(elem.find_all("script", attrs={'type': 'application/ld+json'})[3].contents))[0] for elem in content_posts]