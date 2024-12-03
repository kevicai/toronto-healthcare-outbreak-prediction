# Analyzing the Factors Influencing Outbreak Duration in Toronto Healthcare Institutions

## Overview

This repo presents a comprehensive analysis of outbreak durations in Toronto healthcare institutions between 2016 and 2024. Using Python for data cleaning and preparation, and R for statistical modeling and analysis, the project explores how factors such as outbreak settings, causative agents, and the month of occurrence impact the duration of outbreaks. Through data preprocessing, exploratory analysis, and Bayesian negative binomial regression modeling, the study identifies key drivers of outbreak durations and uncovers patterns and trends.

## File Structure

The repo is structured as:

-   `data/raw_data` contains the raw data as obtained from OpenDataToronto.
-   `data/analysis_data` contains the cleaned dataset that was constructed.
-   `model` contains fitted models. 
-   `other` contains datasheet, details about LLM chat interactions, and sketches.
-   `paper` contains the files used to generate the paper, including the Quarto document and reference bibliography file, as well as the PDF of the paper. 
-   `scripts` contains the R scripts used to simulate, download and clean data.


## Statement on LLM usage

Aspects of the code were written with the help of the auto-complete code tool Tabnine AI and ChatGPT. Parts of the paper were written with the help of ChatGPT, and the entire chat history is available in inputs/llms/usage.txt.
