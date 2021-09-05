import glob
import json
import re
import html
from unidecode import unidecode
from bs4 import BeautifulSoup


files = glob.glob("./data/http_cache/*.html")
download_list = []
for filename in files:
    with open(filename, "r") as page:
        soup = BeautifulSoup(page, 'html.parser')

    print(f"Parsing {filename}")
    
    divs = soup.find_all('div', {'class': 'row zebra rowPadded'})
    for div in divs:
        if 'Style:' in div.text and 'Genre:' in div.text:
            search_str = html.unescape(unidecode((' '.join(div.text.split('\n'))).strip()))
            search_html = html.unescape(unidecode((' '.join(str(div).split('\n'))).strip()))

            try:
                title = re.search("([^<>]*?)Genre:", search_str).group(1) 
            except:
                title = 'error'
            try:
                key = re.search("Key:([^<>]*?)Tuning", search_str).group(1)
            except:
                key = 'error'
            try:
                genre = re.search("Genre: ([^<>]*?)Style", search_str).group(1)
            except:
                genre = 'error'
            try:
                # no y in the style type.
                style = re.search("Style: ([^<>]*?)Key", search_str).group(1)
            except:
                style = 'error'
            try:
                tuning = re.search("Tuning: ([^<>]*?)Difficulty", search_str).group(1)
            except:
                tuning = 'error'
            try:
                # no difficulty level has the the letter 'p' in it.
                difficulty = re.search("Difficulty: ([^<>]*?)Posted", search_str).group(1)
            except:
                difficulty = 'error'
            try:
                # link = re.search("(https://www.hangoutstorage.com.*\.tef)", search_html).group(1)
                urls = re.findall('https://?[\w/\-?=%.]+\.[\w/\-&?=%.]+', search_html)
                link = 'error'
                for url in urls:
                    url = url.strip()
                    if url.endswith('tef'):
                        link = url
                    break
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
with open("./lists/parsed.json", "w") as out:
    out.write(json.dumps(download_list, indent=4))
