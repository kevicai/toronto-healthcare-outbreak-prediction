#### Preamble ####
# Purpose: Models outbreak duration using Bayesian linear regression
# Author: [...UPDATE THIS...]
# Date: [...UPDATE THIS...]
# Contact: [...UPDATE THIS...]
# License: MIT
# Pre-requisites: Install rstanarm library: `install.packages("rstanarm")`

# Load necessary libraries
library(rstanarm)
library(dplyr) # For data manipulation
library(caret) # For splitting data

# Set seed for reproducibility
set.seed(22)

# Read and preprocess the data
input_dir <- "../data/02-analysis_data"
data <- read.csv(file.path(input_dir, "cleaned_data.csv"))

# Convert categorical variables to factors
data <- data %>%
  mutate(
    Outbreak_Setting = factor(Outbreak.Setting),
    Type_of_Outbreak = factor(Type.of.Outbreak),
    Main_Causative_Agent = factor(Main.Causative.Agent),
    Month_Outbreak_Began = Month.Outbreak.Began
  )

# Separate features and target
X <- data %>%
  select(Outbreak_Setting, Type_of_Outbreak, Main_Causative_Agent, Month_Outbreak_Began)
y <- data$Outbreak.Duration.Days

# Combine features and target for splitting
data_model <- data %>%
  select(Outbreak_Setting, Type_of_Outbreak, Main_Causative_Agent, Month_Outbreak_Began, Outbreak.Duration.Days)

# Split the data into train and test sets
train_indices <- createDataPartition(data_model$Outbreak.Duration.Days, p = 0.8, list = FALSE)
train_data <- data_model[train_indices, ]
test_data <- data_model[-train_indices, ]

# Fit the Bayesian linear regression model
model <- stan_glm(
  Outbreak.Duration.Days ~ Outbreak_Setting + Type_of_Outbreak + Main_Causative_Agent + Month_Outbreak_Began,
  data = train_data,
  family = gaussian(),
  prior = normal(0, 2.5),
  seed = 22
)

# Summarize the model
summary(model)

# Make predictions on the test set
y_pred <- predict(model, newdata = test_data)

# Evaluate the model
mse <- mean((test_data$Outbreak.Duration.Days - y_pred)^2)
r2 <- 1 - (sum((test_data$Outbreak.Duration.Days - y_pred)^2) / sum((test_data$Outbreak.Duration.Days - mean(train_data$Outbreak.Duration.Days))^2))

# Print evaluation metrics
cat(sprintf("Mean Squared Error (MSE): %.2f\n", mse))
cat(sprintf("R-squared: %.2f\n", r2))