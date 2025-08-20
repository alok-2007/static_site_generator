import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import json
import re

with open("district_to_postoffices2.json") as dtp1:
    dtp = json.load(dtp1)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template('distTem.html')
clean_url = []

def name_clean(n):
    n = re.sub(r"\'", "-", n)
    n = re.sub(r"\"", "-", n)
    n = re.sub(r"^\s*\.\s*", "", n)
    n = re.sub(r"^\s*\-\s*", "", n)
    n = re.sub(r"\s*\.\s*$", "", n)
    n = re.sub(r"\s*\-\s*$", "", n)
    n = re.sub(r"\s*\-\s*", "-", n)
    n = re.sub(r"\s*\.\s*", ".", n)
    n = re.sub(r"\s*\.\s*(?=\w{2,}\b)", "-", n)
    n = re.sub(r"\.", "", n)
    n = re.sub(r"\-+", "-", n)
    n = re.sub(r"\s+", "-", n)
    n = re.sub(r"\/", "-", n)
    return n.lower()

def post_url_maker(s, d, o):
    s = name_clean(s)
    d = name_clean(d)
    o = name_clean(o)
    return f"{s}/{d}/{o}"

def PostOfficeList_giver(StateName, DistrictName, data):
    PostOfficeList = ""
    PostOfficeList += f"<ol>"
    for office in data:
        PostOfficeList += f"<li><a href='/{post_url_maker(StateName, DistrictName, office)}'>{office.upper()}</a></li>"
    PostOfficeList += f"</ol>"
    return PostOfficeList


for key, data in dtp.items():
    [StateName, DistrictName] = key.split("/")
    key = f"{name_clean(StateName)}/{name_clean(DistrictName)}"

    context = {
        "Slug": key,
        "DistrictName": DistrictName.upper().replace("-", " "),
        "StateName": StateName.upper().replace("-", " "),
        "PostOfficeList": PostOfficeList_giver(StateName, DistrictName, data),
        "TotalPostOffices": len(data)
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
        print(f"😡😡😡😡😡😡😡{key}")

with open("dist_urls.json", "w", encoding="utf-8") as f:
    json.dump(clean_url, f , indent=2)

print("done 👌")