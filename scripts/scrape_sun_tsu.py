#!/usr/bin/env python3
import requests
import yaml
import re

url="http://classics.mit.edu/Tzu/artwar.1b.txt"
response = requests.get(url, stream=True)


current_heading = None
data = []

content, section = "", None
for l in response.iter_lines():

    l = l.decode('utf-8')
    prefix = l.split(' ')[0]

    if "I" in prefix and '.' in prefix :
        print(current_heading)
        current_heading = l
        print(current_heading)

    if len(l) > 0 and l[0].isdigit():
        try:
            section = int(l.split('.')[0])
        except Exception as e:
            section = l.split('.')[0]
        content += ' '.join(l.split('.')[1:]).strip()
    elif section is None:
        continue
    elif len(l) > 0:
        content += ' ' + l.strip()
    elif len(l) == 0:
         d = {
             "title": "Sun Tsu -- Art of War",
             "book": current_heading,
             "section": section,
             "content": content
         }
         data.append(d)
         content = ""
         section = None

open("sun_tsu.yml", "w").write(yaml.dump(data))
