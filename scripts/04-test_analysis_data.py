#### Preamble ####
# Purpose: Tests analysis data
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - 03-clean_data.py
# - Install requirements.txt Python libraries

import pandas as pd
import pytest
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "../data/02-analysis_data/analysis_data.csv"))


def test_column_count():
    assert df.shape[1] == 4, "Dataset does not have 4 columns"


def test_column_types():
    assert df["outbreak_setting"].dtype == "object", "'outbreak_setting' is not string"
    assert df["causative_agent"].dtype == "object", "'causative_agent' is not string"
    assert df["month"].dtype == "object", "'month' is not string"
    assert df["duration"].dtype == "int64", "'duration' is not integer"


def test_no_missing_values():
    # Test that there are no missing values in the dataset.
    assert df.isna().sum().sum() == 0, "Dataset contains missing values"


def test_unique_outbreak_setting():
    unique_outbreaks = len(df["outbreak_setting"].unique())
    assert (
        unique_outbreaks >= 1
    ), "'outbreak_setting' should have at least 1 unique value"


months = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}

def test_month_values():
    # Test that 'month' contains only valid month names.
    
    invalid_months = set(df["month"].unique()) - months # Set difference
    assert not invalid_months, f"Dataset contains invalid months: {invalid_months}"

def test_all_months_present():
    # Test that all 12 months (Jan through Dec) are present in the 'month' column.
    months_present = set(df["month"].unique())
    missing_months = months - months_present # Set difference
    assert not missing_months, f"Dataset is missing months: {missing_months}"
    
def test_duration_positive():
    # Test that 'duration' is positive.
    assert df["duration"].gt(0).all(), "'duration' contains non-positive values"

def test_outbreak_setting_at_least_two_unique():
    # Test that 'outbreak_setting' contains at least two unique values.
    assert (
        len(df["outbreak_setting"].unique()) >= 2
    ), "'outbreak_setting' must contain at least two unique values"


pytest.main(["scripts/04-test_analysis_data.py"])
