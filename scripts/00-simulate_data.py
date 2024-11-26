#### Preamble ####
# Purpose: Simulates a dataset of outbreak data
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - Install requirements.txt Python libraries

#### Workspace setup ####
import pandas as pd
import numpy as np

num_data = 500

# Set random seed for reproducibility
np.random.seed(853)

#### Simulate data ####
# Outbreak settings
outbreak_settings = [
    "Hospital-Chronic Care",
    "Hospital-Psychiatric",
    "LTCH",
    "Retirement Home",
    "Shelter",
    "Transitional Care",
]

# Causative agent groups
causative_agent_groups = [
    "COVID-19",
    "Enterovirus/Rhinovirus",
    "Influenza",
    "Metapneumovirus",
    "Norovirus",
    "Parainfluenza",
    "Respiratory syncytial virus",
]

# Generate the data
outbreak_settings_sampled = np.random.choice(
    outbreak_settings,
    size=num_data,
    replace=True,
)
causative_agents_sampled = np.random.choice(
    causative_agent_groups,
    size=num_data,
    replace=True,
)
months_sampled = np.random.choice(
    list(range(1, 13)),
    size=num_data,
    replace=True,
)
durations_sampled = np.random.randint(
    3,
    21,
    size=num_data,
)  # Random duration between 3 and 20 days

# Create a polars DataFrame
outbreak_data = pd.DataFrame(
    {
        "outbreak_setting": outbreak_settings_sampled,
        "causative_agent": causative_agents_sampled,
        "month": months_sampled,
        "duration": durations_sampled,
    }
)


#### Save data ####
# Write the simulated data to a CSV file
output_dir = "data/00-simulated_data"
outbreak_data.to_csv(f"{output_dir}/simulated_data.csv", index=False)
