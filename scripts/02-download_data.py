#### Preamble ####
# Purpose: Downloads and saves the data from
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites: 
# - install requirements.txt Python libraries

import requests
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../data/01-raw_data")

base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
url = base_url + "/api/3/action/package_show"
params = {"id": "outbreaks-in-toronto-healthcare-institutions"}
package = requests.get(url, params=params).json()

# To get resource data from the recent 3 years, 2022-2024
for idx, resource in enumerate(package["result"]["resources"][:9]):
    if resource["datastore_active"]:
        # To get all records in CSV format:
        url = base_url + "/datastore/dump/" + resource["id"]
        resource_dump_data = requests.get(url).text

       # Save to file
        filename = os.path.join(output_dir, f"{2024 - idx}-data.csv")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(resource_dump_data)
        print(f"Saved to {filename}")