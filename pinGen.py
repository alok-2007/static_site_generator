import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import json
import re

with open("pinTOpost1.json", 'r', encoding="utf-8") as pp1:
    pp = json.load(pp1)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template('pinTem.html')
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

def Slug(d):
    st = name_clean(d[7])
    dis = name_clean(d[6])
    o = name_clean(d[3])
    return f"{st}/{dis}/{o}"

def PostOfficeList_giver(key, data, DistrictSlug, StateSlug):
    PostOfficeList = ""
    for p in data:
        PostOfficeList += f'<section class="postOffice-tab">'
        PostOfficeList += f'<h2 class="lower">{p[3]}, {p[6]}</h2>'
        PostOfficeList += f'<p>Post Office: <span class="pin-span"><a href="/{Slug(p)}">{p[3]}</a></span></p>'
        PostOfficeList += f'<p>Post Office Type: <span class="pin-span">{p[4]}</span></p>'
        PostOfficeList += f'<p>District: <span class="pin-span"><a href="/{DistrictSlug}">{p[6]}</a></span></p>'
        PostOfficeList += f'<p>State: <span class="pin-span"><a href="/{StateSlug}">{p[7]}</a></span></p>'
        PostOfficeList += f'<p>Pin Code: <span class="pin-span"><a href="/{key}">{key}</a></span></p>'
        PostOfficeList += f'<p>Delivery Status: <span class="pin-span">{p[5]}</span></p>'
        PostOfficeList += f'<p>Postal Division: <span class="pin-span">{p[2]}</span></p>'
        PostOfficeList += f'<p>Postal Region: <span class="pin-span">{p[1]}</span></p>'
        PostOfficeList += f'<p>Postal Circle: <span class="pin-span">{p[0]}</span></p>'
        PostOfficeList += f'<p>Latitude: <span class="pin-span">{p[8]}</span></p>'
        PostOfficeList += f'<p>Longitude: <span class="pin-span">{p[9]}</span></p>'
        PostOfficeList += f'</section>'
    return PostOfficeList

os.makedirs("Pincodes", exist_ok=True)

for key, data in pp.items():

    context = {
        "Pincode": key,
        "DistrictName": data[0][6],
        "StateName": data[0][7],
        "TotalOffice": len(data),
        "PostOfficeList": PostOfficeList_giver(key, data, f"{data[0][7].lower().replace(" ", "-")}/{data[0][6].lower().replace(" ", "-")}", data[0][7].lower().replace(" ", "-"))
    }

    html_content = template.render(**context)

    filename = f'{key}.html'
    file_path = os.path.join("Pincodes", filename)
    try:
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(html_content)
        print(f"{key} - done")
        clean_url.append(f"https://searchpincode.in/{key}")
    except OSError as e:
        print(f'😡😡😡😡😡😡😡')
    

with open("pincode_url.json", 'w', encoding='utf-8') as f:
    json.dump(clean_url, f, indent=2)

print("done👌")
