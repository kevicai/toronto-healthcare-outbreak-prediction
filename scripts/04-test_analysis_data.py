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
    assert df["Outbreak Setting"].dtype == "object", "'Outbreak Setting' is not string"
    assert (
        df["Causative Agent Group"].dtype == "object"
    ), "'Causative Agent Group' is not string"
    assert (
        df["Month Outbreak Began"].dtype == "int64"
    ), "'Month Outbreak Began' is not integer"
    assert (
        df["Outbreak Duration Days"].dtype == "int64"
    ), "'Outbreak Duration Days' is not integer"


def test_no_missing_values():
    # Test that there are no missing values in the dataset.
    assert df.isna().sum().sum() == 0, "Dataset contains missing values"


def test_unique_outbreak_setting():
    unique_outbreaks = len(df["Outbreak Setting"].unique())
    assert (
        unique_outbreaks >= 1
    ), "'Outbreak Setting' should have at least 1 unique value"


def test_month_range():
    # Test that 'Month Outbreak Began' is in the valid range 1-12.
    assert (
        df["Month Outbreak Began"].between(1, 12).all()
    ), "'Month Outbreak Began' contains invalid values"


def test_outbreak_duration_positive():
    # Test that 'Outbreak Duration Days' is positive.
    assert (
        df["Outbreak Duration Days"] > 0
    ).all(), "'Outbreak Duration Days' contains non-positive values"


def test_party_at_least_two_unique():
    # Test that 'Outbreak Setting' contains at least two unique values.
    assert (
        len(df["Outbreak Setting"].unique()) >= 2
    ), "'Outbreak Setting' must contain at least two unique values"


pytest.main(["scripts/04-test_analysis_data.py"])
