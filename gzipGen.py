import gzip
import shutil
import os

directory = "SiteMap_dir"

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        xml_path = os.path.join(directory, filename)
        gzip_path = xml_path + ".gz"

        with open(xml_path, 'rb') as f_in:
            with gzip.open(gzip_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f"done: {filename} > {filename}.gz")