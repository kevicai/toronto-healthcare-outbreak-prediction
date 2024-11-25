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
combined_df["Outbreak Duration Days"] = (
    combined_df["Date Declared Over"] - combined_df["Date Outbreak Began"]
).dt.days

# Extract the month of the start of the outbreak
combined_df["Month Outbreak Began"] = combined_df["Date Outbreak Began"].dt.month

# Rename the "Causative Agent-1" column to "Main Causative Agent"
combined_df["Main Causative Agent"] = combined_df["Causative Agent-1"]

# Select required columns
df = combined_df[
    [
        "Outbreak Setting",
        "Main Causative Agent",
        "Month Outbreak Began",
        "Outbreak Duration Days",
    ]
]

# unique causative agents
# unique_values = sorted(
#     df_cleaned["Main Causative Agent"].unique()
# )  # original 55 agents
# print(len(unique_values))
# for value in unique_values:
#     print(value)

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


def group_causative_agent(agent):
    mapping = reverse_mapping.get(agent, "Other")
    # if mapping == "Other":
    #     print(agent)
    return mapping

df["Causative Agent Group"] = df["Main Causative Agent"].apply(group_causative_agent)

df["Outbreak Duration Days"] = df["Outbreak Duration Days"].apply(int)

# Filter uninformative rows
df = df[df["Causative Agent Group"] != "Other"]

# Count rows after removing invalid data
rows_after = df.shape[0]
rows_removed = rows_before - rows_after

value_counts = df["Causative Agent Group"].value_counts()
print(value_counts)

# top_10 = (
#     df["Main Causative Agent"]
#     .value_counts()
#     .sort_values()  # Sort by counts in descending order
#     .head(10)
# )
# print(top_10)

df = df[
    [
        "Outbreak Setting",
        "Causative Agent Group",
        "Month Outbreak Began",
        "Outbreak Duration Days",
    ]
]

print(f"Number of rows with N/A data removed: {rows_removed}")  # 31

# Save the cleaned dataframe as CSV
os.makedirs(output_dir, exist_ok=True)
cleaned_filename = os.path.join(output_dir, "analysis_data.csv")
df.to_csv(cleaned_filename, index=False)
print(f"Cleaned data saved to {cleaned_filename}")
