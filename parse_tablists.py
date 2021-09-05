import glob
import json
import re
from bs4 import BeautifulSoup

files = glob.glob("./http_cache/*.html")
download_list = []
for filename in files:
    with open(filename, "r") as page:
        soup = BeautifulSoup(page, 'html.parser')

    print(f"Parsing {filename}")
    
    divs = soup.find_all('div', {'class': 'row zebra rowPadded'})
    for div in divs:
        if 'Style:' in div.text and 'Genre:' in div.text:
            search_str = ' '.join(div.text.split('\n')).strip()
            search_html = ' '.join(str(div).split('\n')).strip()

            try:
                title = re.search("(.*)Genre:", search_str).group(1) 
            except:
                title = 'error'
            try:
                key = re.search("Key:(.*)Tuning", search_str).group(1)
            except:
                key = 'error'
            try:
                genre = re.search("Genre: (.*)Style", search_str).group(1)
            except:
                genre = 'error'
            try:
                style = re.search("Style: (.*)Key", search_str).group(1)
            except:
                style = 'error'
            try:
                tuning = re.search("Tuning: (.*)Difficulty", search_str).group(1)
            except:
                tuning = 'error'
            try:
                difficulty = re.search("Difficulty: (.*)Posted", search_str).group(1)
            except:
                difficulty = 'error'
            try:
                link = re.search("(https://www.hangoutstorage.com.*\.tef)", search_html).group(1)
            except:
                link = 'error'

            download_list.append(
                {
                    'filename': filename,
                    'title': title.strip(),
                    'key': key.strip(),
                    'genre': genre.strip(),
                    'style': style.strip(),
                    'tuning': tuning.strip(),
                    'difficulty': difficulty.strip(),
                    'link': link.strip(),
                    'search_str': search_str,
                    'search_html': search_html
                }
            )
        else:
            continue
with open("parsed.json", "w") as out:
    out.write(json.dumps(download_list, indent=4))
