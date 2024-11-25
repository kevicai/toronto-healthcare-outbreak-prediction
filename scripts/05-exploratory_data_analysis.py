#### Preamble ####
# Purpose: Explores the analysis data
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - 03-clean_data.py
# - Install requirements.txt Python libraries

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "../data/02-analysis_data/analysis_data.csv"))

# See unique settings
unique_values = sorted(df["Type of Outbreak"].unique()) 
print(len(unique_values))
for value in unique_values:
    print(value)
