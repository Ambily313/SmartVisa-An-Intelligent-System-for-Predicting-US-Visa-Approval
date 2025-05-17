# SmartVisa - An Intelligent System for Predicting US Visa Approval

##  Project Overview
SmartVisa is a machine learning-based project designed to predict the outcome of US visa applications based on various applicant and employment features. It helps users assess their chances of approval and can be extended to other binary classification use cases.

---

##  Problem Statement
To predict whether a US visa application will be **approved or denied** based on features such as:

- 🌍 Continent: Asia, Africa, North America, etc.
- 🎓 Education Level: High School, Bachelor’s, Master’s, Doctorate
- 👨‍💼 Job Experience: Yes/No
- 📚 Training Required: Yes/No
- 🏢 Number of Employees: 15,000–40,000
- 🌐 Region of Employment: West, Northeast, etc.
- 💰 Prevailing Wage: 700–70,000
- ⏱️ Contract Tenure: Hour, Month, Week, Year
- 🕒 Full-time Employment: Yes/No
- 🏗️ Age of Company: 15–180

---

##  Objectives

- Predict visa approval status accurately.
- Build a robust and modular ML pipeline.
- Deploy the application for real-time predictions via a user-friendly web interface.
- Enable end-to-end automation using cloud and CI/CD tools.

---

##  Project Architecture

### ✔ Major Components

1. **Add Data to MongoDB** – Store raw data in a NoSQL database for scalability.
2. **Folder Structure** – Organize codebase into modular components for reusability and maintainability.
3. **Custom Logging & Exception Handling** – Implement centralized logging and exception tracking.
4. **MongoDB Integration** – Use MongoDB for storing and querying datasets.
5. **Data Ingestion** – Fetch data from MongoDB and convert to pandas DataFrame for processing.
6. **Evidently Integration** – Profile the data to track distribution shifts and schema drift.
7. **Data Validation** – Validate schema, nulls, and data types to ensure clean input.
8. **Data Transformation** – Encode categorical features, scale numerical columns, and prepare train-test splits.
9. **Model Training** – Train models like Logistic Regression, Random Forest, XGBoost, and CatBoost.
10. **AWS Connection** – Connect and push artifacts to AWS S3.
11. **Model Evaluation** – Compare model metrics (accuracy, precision, recall, F1-score) and select the best model.
12. **Model Pusher** – Save and push the final trained model to S3 for deployment.
13. **Training Pipeline** – Orchestrate the entire training workflow automatically.
14. **Prediction Pipeline** – Load saved model and predict on real-time user inputs.
15. **App Design** – Design a frontend with input fields to make predictions accessible via a web app.

---

##  Deployment & Automation

- **Containerization**: Dockerized for portability
- **Cloud**: AWS EC2 (App Hosting), AWS S3 (Model Storage)
- **CI/CD**: GitHub Actions with YAML workflows and self-hosted runners for automation
- **Web Framework**: Flask for RESTful API deployment

---

##  Tech Stack

| Category | Tools |
|---------|-------|
| Language | Python |
| ML Libraries | Pandas, Scikit-learn, XGBoost, CatBoost, Matplotlib |
| Deployment | Flask, Docker |
| Cloud | AWS EC2, AWS S3 |
| Automation | GitHub Actions |
| Database | MongoDB |
| Logging | Custom Logging Module |
| Monitoring | Evidently AI |

---

## 🔄 Workflow Summary

MongoDB → Data Ingestion → Validation → Transformation
→ Model Training → Evaluation → Pusher → AWS S3
→ Training & Prediction Pipelines → Frontend App → AWS EC2

## 📝 Future Improvements

- Integration with advanced deep learning models (e.g., LSTM or Transformer-based for time-aware features)
- Real-time monitoring and feedback system
- Enhanced dataset with more diverse features
- API Gateway integration for mobile app consumption
