import json
import requests
import re

with open('./parsed.json', 'r') as f:
    download_list = json.load(f)

raw_tab_list = []

for index, item in enumerate(download_list):
    item['tab'] = 'error'

    if item['link'] == 'error':
        continue
    else:
        tabname = re.search(
                'https://www.hangoutstorage.com/banjohangout.org/storage/tabs/.*/(.*\.tef)',
                item['link']).group(1)
        resp = requests.get(item['link'])
        outfile = f"./raw_tabs/{tabname}".strip()
        with open(outfile, "wb") as f:
            f.write(resp.content)
        print("Downloaded:", item['link'])

        raw_tab_list.append({
            'filename': item['filename'],
            'title': item['title'],
            'key': item['key'],
            'genre': item['genre'],
            'style': item['style'],
            'tuning': item['tuning'],
            'difficulty': item['difficulty'],
            'raw_tab': outfile,
            'link': item['link']
        })

with open('raw_tab_list.json', 'w') as f:
    f.write(json.dumps(raw_tab_list, indent=4))
