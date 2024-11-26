#### Preamble ####
# Purpose: Splits analysis data into training and testing
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - 03-clean_data.py
# - Install required R packages: 'dplyr', 'caret'

library("dplyr")
library("caret")

# Set seed for reproducibility
set.seed(22)

# Read and preprocess the data
input_dir <- "./data/02-analysis_data"
data <- read.csv(file.path(input_dir, "analysis_data.csv"))

# Split the data into training and test sets (80-20 split)
train_indices <- createDataPartition(data$duration, p = 0.8, list = FALSE)
train_data <- data[train_indices, ]
test_data <- data[-train_indices, ]

# Save the training and test sets to CSV
write.csv(train_data, file = "./data/02-analysis_data/train_data.csv", row.names = FALSE)
write.csv(test_data, file = "./data/02-analysis_data/test_data.csv", row.names = FALSE)