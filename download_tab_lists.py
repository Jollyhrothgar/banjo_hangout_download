"""
This script just creates a local copy of all html pages so that they can be parsed later.
"""

import json
import requests

with open ("./lists/url_list.json", "r") as url_list:
    urls = json.load(url_list)


for counter, url in enumerate(urls):
    print(f"Scraping URL: {url}")
    response = requests.get(url)
    
    with open(f"./data/http_cache/{counter}.html", "w") as out:
        out.write(response.text)
    print("...done!")

