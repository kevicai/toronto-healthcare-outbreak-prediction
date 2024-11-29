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

sample_size = 1000

# Set random seed for reproducibility
np.random.seed(22)

#### Define Data Categories ####
# Outbreak settings
outbreak_settings = [
    "Hospital-Chronic Care",
    "Hospital-Psychiatric",
    "Hospital−Acute Care",
    "LTCH",
    "Retirement Home",
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
    "Coronavirus",
]

#### Simulate data ####
outbreak_settings_sampled = np.random.choice(
    outbreak_settings,
    size=sample_size,
    replace=True,
)

causative_agents_sampled = np.random.choice(
    causative_agent_groups,
    size=sample_size,
    replace=True,
)

months_sampled = np.random.choice(
    list(range(1, 13)),
    size=sample_size,
    replace=True,
)

# Simulate durations using a normal distribution
mean_duration = 14  
std_duration = 14   
durations_sampled = np.random.normal(loc=mean_duration, scale=std_duration, size=sample_size)

# Create a Pandas DataFrame
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
