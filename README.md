# SmartVisa-An-Intelligent-System-for-Predicting-US-Visa-Approval

## Project Overview

This project aims to predict whether a US visa application will be approved based on various applicant features using machine learning and deep learning models. It is designed to help applicants assess their chances and improve their eligibility.

---


## Problem Statement

The goal is to predict whether a US visa application will be approved based on input features like:

- Continent (Asia, Africa, North America, etc.)
- Education Level (High School, Bachelor’s, Master’s, Doctorate)
- Job Experience (Yes/No)
- Training Required (Yes/No)
- Number of Employees (15,000–40,000)
- Region of Employment (West, Northeast, etc.)
- Prevailing Wage (700–70,000)
- Contract Tenure (Hour, Month, Week, Year)
- Full-time (Yes/No)
- Age of Company (15–180)

---

## Application Scope

- Can be used by real US visa applicants to estimate their visa approval chances.
- The methodology is extendable to other binary classification problems in ML.

---

## Solution Approach

1. Load the US visa dataset.
2. Perform Exploratory Data Analysis (EDA) and feature extraction.
3. Apply classification algorithms such as Logistic Regression, SVC, Random Forest, XGBoost, and CatBoost.
4. Evaluate and select top-performing models.
5. Perform hyperparameter tuning.
6. Choose the best model based on performance metrics.

---

## Project Structure

###  Components

- **Data Ingestion**
- **Data Validation**
- **Data Transformation**
- **Model Trainer**
- **Model Evaluation**
- **Model Pusher**
- **Training Pipeline**
- **Prediction Pipeline**
- **Frontend Application**

---

## Deployment Overview

- **Containerization:** Docker
- **Cloud Platforms:** AWS EC2, AWS S3
- **CI/CD:** GitHub Actions with self-hosted runner
- **Workflow Automation:** YAML-based GitHub workflows

---

## Prerequisites

### Notebook

- Python
- Anaconda/Miniconda
- GitHub
- Basic understanding of ML algorithms

### Application

- Flask (for building REST APIs)

### Deployment

- Docker
- AWS EC2, AWS S3

---

## Conclusion

- The solution showcases the application of classification ML models for visa approval prediction.
- Potential improvements can include broader datasets, advanced deep learning models, or real-time API integration.


---
