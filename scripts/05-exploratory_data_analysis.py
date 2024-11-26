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
unique_values = sorted(df["outbreak_setting"].unique())
print(len(unique_values))
for value in unique_values:
    print(value)

# See unique causative agents
unique_values = sorted(df["causative_agent"].unique())  # original 55 agents
print(len(unique_values))
for value in unique_values:
    print(value)

# Top 10 agents
top_10 = (
    df["causative_agent"]
    .value_counts()
    .sort_values()  # Sort by counts in descending order
    .head(10)
)
print(top_10)

# Count causative agents occurances
value_counts = df["causative_agent"].value_counts()
print(value_counts)