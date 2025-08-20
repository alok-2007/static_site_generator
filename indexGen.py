import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import json
import re

df = pd.read_csv("pincode.csv")

stateList = df["StateName"].unique()

env = Environment(loader=FileSystemLoader("."))
template = env.get_template('indexTem.html')

def StateList_giver(sL):
    StateList = ""
    StateList += f"<ol>"
    for st in sL:
        StateList += f"<li><a href='/{st.lower().replace(" ", "-")}'>{st}</a></li>"
    StateList += f"</ol>"
    return StateList

context = {
    "StateList": StateList_giver(sorted(stateList))
}

html_content = template.render(**context)

filename = "./index.html"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(html_content)

print("done 👌")