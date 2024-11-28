#### Preamble ####
# Purpose: Cleans the raw outbreak data
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - 02-download_data.py
# - Install requirements.txt Python libraries

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(script_dir, "../data/01-raw_data")
output_dir = os.path.join(script_dir, "../data/02-analysis_data")

# Combine 2016 to 2024 files
filenames = [os.path.join(input_dir, f"{year}-data.csv") for year in range(2016, 2025)]

# Initialize an empty list for DataFrames
dataframes = []

# Read each file into a DataFrame and append it to the list
for filename in filenames:
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        dataframes.append(df)
    else:
        print(f"File {filename} does not exist.")

# Combine all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Convert time to datetime format
combined_df["Date Outbreak Began"] = pd.to_datetime(
    combined_df["Date Outbreak Began"], format="%Y-%m-%d", errors="coerce"
)
combined_df["Date Declared Over"] = pd.to_datetime(
    combined_df["Date Declared Over"], format="%Y-%m-%d", errors="coerce"
)

# Calculate the difference in days and create a new column
combined_df["duration"] = (
    combined_df["Date Declared Over"] - combined_df["Date Outbreak Began"]
).dt.days

# Extract the month of the start of the outbreak
combined_df["month"] = combined_df["Date Outbreak Began"].dt.month

# Rename variables
combined_df["Main Causative Agent"] = combined_df["Causative Agent-1"]
combined_df["outbreak_setting"] = combined_df["Outbreak Setting"]

# Select required columns
df = combined_df[
    [
        "outbreak_setting",
        "Main Causative Agent",
        "month",
        "duration",
    ]
]

# Define grouping rules:
group_mapping = {
    "Influenza": [
        "Influenza A ((H1N1)pdm09)",
        "Influenza A (H1)",
        "Influenza A (H1N1)",
        "Influenza A (H3)",
        "Influenza A (H3N2)",
        "Influenza A (Not subtyped)",
        "Influenza A (H3)",
        "Influenza A (H3), Parainfluenza type 2",
        "Influenza A (H3), Parainfluenza type 1",
        "Influenza A and B",
        "Influenza B",
    ],
    "Respiratory syncytial virus": [
        "Respiratory syncytial virus",
    ],
    "Metapneumovirus": [
        "Metapneumovirus",
    ],
    "Enterovirus/Rhinovirus": [
        "Rhinovirus",
        "Enterovirus",
        "Enterovirus/ Rhinovirus",
        "Enterovirus/Rhinovirus",
    ],
    "COVID-19": [
        "COVID-19",
    ],
    "Coronavirus": [
        "Coronavirus",
        "Coronavirus*",
    ],
    "Parainfluenza": [
        "Parainfluenza",
        "Parainfluenza type 1",
        "Parainfluenza Type 1",
        "Parainfluenza type 2",
        "Parainfluenza type 3",
        "Parainfluenza type 4",
        "Parainfluenza PIV III",
        "Parainfluenza virus",
        "Parainfluenza UNSPECIFIED",
    ],
    "Norovirus": ["Norovirus", "Norovirus-like"],
}
reverse_mapping = {
    agent: group for group, agents in group_mapping.items() for agent in agents
}

# Remove rows with invalid data (null values)
rows_before = df.shape[0]

# Filter invalid or uninformative rows
df = df.dropna()
df = df[df["Main Causative Agent"] != "Unable to identify"]
df = df[~df["outbreak_setting"].isin(["Shelter", "Transitional Care"])]

def group_causative_agent(agent):
    mapping = reverse_mapping.get(agent, "Other")
    # if mapping == "Other":
    #     print(agent)
    return mapping

df["causative_agent"] = df["Main Causative Agent"].apply(group_causative_agent)

df["duration"] = df["duration"].apply(int)

# Filter uninformative rows
df = df[df["causative_agent"] != "Other"]

# Count rows after removing invalid data
rows_after = df.shape[0]
rows_removed = rows_before - rows_after

# Map month number to text
month_mapping = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}
df["month"] = df["month"].map(month_mapping)

df = df[
    [
        "outbreak_setting",
        "causative_agent",
        "month",
        "duration",
    ]
]

print(f"Number of rows with N/A data removed: {rows_removed}")  # 31

# Save the cleaned dataframe as CSV
os.makedirs(output_dir, exist_ok=True)
cleaned_filename = os.path.join(output_dir, "analysis_data.csv")
df.to_csv(cleaned_filename, index=False)
print(f"Cleaned data saved to {cleaned_filename}")
