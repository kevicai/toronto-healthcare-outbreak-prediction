#### Preamble ####
# Purpose: Load previously saved models and perform model checks and evaluations
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - 07-model_data.R
# - Install required R packages: 'rstanarm', 'dplyr', 'caret', 'loo'

# Load the previously saved models
poisson_model <- readRDS("models/poisson_model.rds")
neg_binomial_model <- readRDS("models/neg_binomial_model.rds")

# Load test data from CSV
test_data <- read.csv("data/02-analysis_data/test_data.csv")
test_data <- test_data %>%
  mutate(
    outbreak_setting = factor(outbreak_setting),
    causative_agent = factor(causative_agent),
    month = factor(month)
  )

# Posterior predictive checks
pp_check(poisson_model) +
  theme(legend.position = "bottom")

pp_check(neg_binomial_model) +
  theme(legend.position = "bottom")

# Compare the models using LOO (Leave-One-Out Cross Validation)
poisson_loo <- loo(poisson_model, cores = 2)
neg_binomial_loo <- loo(neg_binomial_model, cores = 2)

loo_comparison <- loo_compare(poisson_loo, neg_binomial_loo)
print(loo_comparison)

# Summarize the results of the LOO comparison
cat("Summary of LOO Comparison:\n")
cat("ELPD Difference:", loo_comparison$elpd_diff, "\n")
cat("SE Difference:", loo_comparison$se_diff, "\n")

# Make predictions on the test data
poisson_pred <- predict(poisson_model, newdata = test_data, type = "response")

neg_binomial_pred <- predict(neg_binomial_model, newdata = test_data, type = "response")

# Calculate MAE for models
mae_poisson <- mean(abs(test_data$duration - poisson_pred))

mae_neg_binomial <- mean(abs(test_data$duration - neg_binomial_pred))

# Print metrics for comparison
cat("MAE for Poisson model: ", mae_poisson, "\n")
cat("MAE for Negative Binomial model: ", mae_neg_binomial, "\n")