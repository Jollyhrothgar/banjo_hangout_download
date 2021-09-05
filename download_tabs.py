import json
import requests
import re
import pandas as pd

with open('./lists/parsed.json', 'r') as f:
    download_list = json.load(f)

tabs = pd.DataFrame.from_records(download_list)

tabs['filename_base'] = tabs['title'].apply(lambda x: '_'.join((x.lower().replace('?','').replace('(', ' ').replace(')', ' ').replace('/',' ').replace('\\', ' ').strip().split()[0:5]))) + tabs['difficulty'].apply(lambda x: "_" + x.lower() if x.lower() != 'error' else '') 

valid_tabs = tabs[tabs['link'] != 'error']
names = valid_tabs['filename_base'].unique()

tab_status = []

for name in names:
    for idx, (row_idx, row) in enumerate(valid_tabs[valid_tabs['filename_base'] == name].iterrows()):
        download_link = row.loc['link']
        file_prefix = row.loc['filename_base']
        outfile = f"./data/tabs/{file_prefix}_{idx:03d}.tef"

        print(f"Downloading {download_link} and saving to {outfile}")
        resp = requests.get(download_link)
        
        if resp.status_code == 200:
            # We're good!
            with open(outfile, "wb") as f:
                f.write(resp.content)
            tab_status.append({
                'filename': row['filename'],
                'title': row['title'],
                'key': row['key'],
                'genre': row['genre'],
                'style': row['style'],
                'tuning': row['tuning'],
                'difficulty': row['difficulty'],
                'downloaded_tab': outfile,
                'link': row['link'],
                'http_status': resp.status_code
            })
        else:
            # We're not good!
            print("...Error, HTTP Status: ", resp.status_code)
            tab_status.append({
                'filename': row['filename'],
                'title': row['title'],
                'key': row['key'],
                'genre': row['genre'],
                'style': row['style'],
                'tuning': row['tuning'],
                'difficulty': row['difficulty'],
                'downloaded_tab': 'error',
                'link': row['link'],
                'http_status': resp.status_code
            })

        print('...Done!')


with open('./lists/tabs.json', 'w') as f:
    f.write(json.dumps(tab_status, indent=4))
