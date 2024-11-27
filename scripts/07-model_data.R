#### Preamble ####
# Purpose: Models outbreak duration using Negative Binomial and Poisson regression
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - 06-split_data.py
# - Install required R packages: 'rstanarm', 'dplyr', 'caret', 'loo'

library(rstanarm)
library(dplyr)
library(caret)
library(modelsummary)
library(loo)

# Set seed for reproducibility
set.seed(22)

# Load the previously saved training and test data
train_data <- read.csv("./data/02-analysis_data/train_data.csv")

# Convert categorical variables to factors
train_data <- train_data %>%
  mutate(
    outbreak_setting = factor(outbreak_setting),
    causative_agent = factor(causative_agent),
    month = factor(month)
  )

# Separate the features and target variable for modeling
X <- train_data %>%
  select(outbreak_setting, causative_agent, month)
y <- train_data$duration

# Fit Poisson and Negative Binomial models
poisson_model <- stan_glm(
  duration ~ outbreak_setting + causative_agent + month,
  data = train_data,
  family = poisson(link = "log"),
  prior = normal(location = 0, scale = 2.5, autoscale = TRUE),
  prior_intercept = normal(location = 0, scale = 2.5, autoscale = TRUE),
  seed = 22
)

neg_binomial_model <- stan_glm(
  duration ~ outbreak_setting + causative_agent + month,
  data = train_data,
  family = neg_binomial_2(link = "log"),
  prior = normal(location = 0, scale = 2.5, autoscale = TRUE),
  prior_intercept = normal(location = 0, scale = 2.5, autoscale = TRUE),
  seed = 22
)

# Save the models for later use
saveRDS(poisson_model, file = "models/poisson_model.rds")
saveRDS(neg_binomial_model, file = "models/neg_binom_model.rds")
