import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import json
import re

with open("districts.json") as dist1:
    dist = json.load(dist1)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template('stateTem.html')
clean_url = []

def name_clean(n):
    n = re.sub(r"^\s*\.\s*", "", n)
    n = re.sub(r"^\s*\-\s*", "", n)
    n = re.sub(r"\s*\.\s*$", "", n)
    n = re.sub(r"\s*\-\s*$", "", n)
    n = re.sub(r"\s*\-\s*", "-", n)
    n = re.sub(r"\s*\.\s*", ".", n)
    n = re.sub(r"\s*\.\s*(?=\w{2,}\b)", "-", n)
    n = re.sub(r"\.", "", n)
    n = re.sub(r"\s+", "-", n)
    n = re.sub(r"\/", "-", n)
    return n.lower()


def DistrictList_giver(key, data):
    DistrictList = ""
    DistrictList += f"<ol>"
    for dis in data:
        DistrictList += f"<li><a href='/{key}/{name_clean(dis)}'>{dis}</a></li>"
    DistrictList += f"</ol>"
    return DistrictList

for key, data in dist.items():
    key = name_clean(key)
    context = {
        "StateName": key.upper().replace("-", " "),
        "Slug": key,
        "DistrictList": DistrictList_giver(key, data),
        "DistrictCount": len(data)
    }

    html_content = template.render(**context)

    filename = f"states/{key}/index.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"{key} - done")
        clean_url.append(f"https://searchpincode.in/{key}")
    except OSError as e:
        print(f"😡😡😡😡😡{key}")
    
with open("state_urls.json", "w", encoding="utf-8") as f:
    json.dump(clean_url, f, indent=2)

print("done 👌")