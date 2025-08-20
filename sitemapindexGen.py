import json
import xml.etree.ElementTree as ET
from datetime import date
import os

# Load sitemap URLs from JSON file
with open("sitemap-url.json", "r") as f:
    sitemap_urls = json.load(f)

# Create the root <sitemapindex> element
sitemap_index = ET.Element("sitemapindex", {
    "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"
})

# Add each sitemap URL as a <sitemap> element
for url in sitemap_urls:
    sitemap = ET.SubElement(sitemap_index, "sitemap")
    
    loc = ET.SubElement(sitemap, "loc")
    loc.text = f"https://searchpincode.in/{url}"

    lastmod = ET.SubElement(sitemap, "lastmod")
    lastmod.text = date.today().isoformat()

# Write to sitemap-index.xml
tree = ET.ElementTree(sitemap_index)
os.makedirs("SiteMap_dir", exist_ok=True)
file_name = "SiteMap_dir/sitemap-index.xml"
tree.write(file_name, encoding="utf-8", xml_declaration=True)

print("✅ sitemap-index.xml generated!")
