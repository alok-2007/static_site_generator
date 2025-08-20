import sys
import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import json
import re

df = pd.read_csv("States_vill/Rajasthan_vill.csv")
with open("pinTOpost1.json", "r", encoding="utf-8") as f:
    jd = json.load(f)

state_for_url = df['stateNameEnglish'].unique()[0]

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('villTem.html')
clean_url = []
nu = 17

def get_village(villageName):
    villageName = re.sub(r"[()]", " ", villageName).lower()
    villageName = villageName.replace("*", "")
    villageName = re.sub(r"^\s*\-\s*", "", villageName)
    villageName = re.sub(r"\s*\-\s*$", "", villageName)
    villageName = re.sub(r"\s*\-\s*", "-", villageName)
    villageName = re.sub(r'\"', " ", villageName)
    if "." in villageName:
        villageName = re.sub(r"\s*\.\s*$", "", villageName)
        villageName = re.sub(r"^\s*\.\s*", "", villageName)
        villageName = re.sub(r"\s\.\s", " ", villageName)
        villageName = re.sub(r"\s*\.\s*(?=([a-z0-9\-]{2,}))", " \1", villageName)
        villageName = re.sub(
            r'(?:\b([a-zA-Z])\.\s*)+',
            lambda m: ''.join(re.findall(r'[a-zA-Z]', m.group(0))),
            villageName
        )
        villageName = re.sub(r'\s*\.\s*', '-', villageName)
        villageName = re.sub(r'\.-*$', '', villageName)
    villageName = re.sub(r"\s+", "-", villageName).strip()
    villageName = re.sub(r"\.+", "", villageName)
    villageName = re.sub(r"\/+", "-", villageName)
    villageName = re.sub(r"[^a-zA-Z0-9\-]", "", villageName)
    villageName = re.sub(r"\-+", "-", villageName)
    villageName = re.sub(r"^\-", "", villageName)
    villageName = re.sub(r"\-$", "", villageName)
    return villageName.strip()

def make_slug(data):
    vill = get_village(data["villageNameEnglish"])
    sub_dist_raw = data['subdistrictNameEnglish']
    dist_raw = data['districtNameEnglish']
    state_raw = data['stateNameEnglish']
    pincode = data['pincode']

    sub_dist_processed = get_village(sub_dist_raw.replace('/', "-"))
    dist_processed = get_village(dist_raw)
    state_processed = get_village(state_raw.replace(" ", "-"))

    subdist = ""
    if sub_dist_processed == dist_processed:
        subdist = dist_processed
    else:
        subdist = f"{sub_dist_processed}-{dist_processed}"

    return f"{vill}-{subdist}-{state_processed}-{pincode}"


def samepincode_giver(pincode, vill):
    flt_df = df[df["pincode"] == pincode]
    villageOfPincode = ""
    for _, row in flt_df.iterrows():
        if not vill == row["villageNameEnglish"]:
            villageOfPincode += f"<a href='/{make_slug(row)}'>{row["villageNameEnglish"]}, {row['districtNameEnglish']}</a>  "
    return villageOfPincode.strip()

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

def postoffice_giver(pincode):
    flt_jd = jd.get(str(pincode))
    if not flt_jd:
        return "Post Office Not Found for This PIN Code"
    postOfficeOfPincode = ""
    for arr in flt_jd:
        postOfficeOfPincode += f"<a href='/{post_url_maker(arr[7], arr[6], arr[3])}'>{arr[3]}</a>  "
    return postOfficeOfPincode

os.makedirs("villages", exist_ok=True)
os.makedirs(f"villages/{nu}", exist_ok=True)

for index, v in df.iterrows():
    slug = make_slug(v)

    context = {
        "slug": slug,
        "villageOfPincode": samepincode_giver(v['pincode'], v['villageNameEnglish']),
        "postOfficeOfPincode": postoffice_giver(v['pincode']),
        "stateLower": v['stateNameEnglish'].lower().replace(" ", "-"),
        "districtLower": v['districtNameEnglish'].lower().replace(" ", "-"),
        "stateCode": v['stateCode'],
        "stateNameEnglish": v['stateNameEnglish'].upper(),
        "districtCode": v['districtCode'],
        "districtNameEnglish": v['districtNameEnglish'].upper(),
        "subdistrictCode": v['subdistrictCode'],
        "subdistrictNameEnglish": v['subdistrictNameEnglish'].upper(),
        "villageCode": v['villageCode'],
        "villageNameEnglish": v['villageNameEnglish'].upper(),
        "pincode": v['pincode'],
        "villageC": v['villageNameEnglish'].title(),
        "subdistrictC": v['subdistrictNameEnglish'].title(),
        "districtC": v['districtNameEnglish'].title(),
        "stateC": v['stateNameEnglish'].title()
    }

    html_content = template.render(**context)

    filename = f"{slug}.html"
    file_path = os.path.join(f"villages/{nu}", filename)
    with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    print(f"{index}, {slug}, done")
    clean_url.append(f"https://searchpincode.in/{slug}")

with open(f"{state_for_url.replace(" ", "-").lower()}_url.json", "w", encoding="utf-8") as f:
    json.dump(clean_url, f, indent=2)

print("done👌")