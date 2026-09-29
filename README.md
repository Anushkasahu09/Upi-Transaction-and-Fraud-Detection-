# 💳 UPI Transaction and Fraud Detection

A **rule-based UPI transaction fraud detection and risk analysis system** developed using Python, Pandas, MySQL, SQL, and Streamlit.

The project analyzes UPI transactions and identifies potentially suspicious transactions using predefined fraud detection rules based on transaction amount, transaction time, device type, network type, and weekend activity.

## 📌 Project Overview

Digital payment systems such as UPI process a large number of transactions every day. Detecting unusual or potentially fraudulent transactions is important for improving transaction security.

This project provides a simple **Rule-Based Fraud Detection System** that assigns a **Risk Score** to every transaction and categorizes it into:

* 🟢 **Low Risk**
* 🟡 **Medium Risk**
* 🔴 **High Risk**

The project does **not use Machine Learning**. Instead, it uses predefined business rules and SQL queries to identify suspicious transaction patterns.

## 🎯 Objectives

* Analyze UPI transaction data.
* Identify suspicious transaction patterns.
* Calculate a risk score for each transaction.
* Categorize transactions according to their risk level.
* Store and manage transaction data using MySQL.
* Perform SQL-based fraud analysis.
* Visualize transaction patterns using an interactive Streamlit dashboard.
* Provide a simple transaction risk analysis system.

## 🛠️ Technologies Used

| Technology           | Purpose                                     |
| -------------------- | ------------------------------------------- |
| **Python**           | Data processing and application development |
| **Pandas**           | Data cleaning and analysis                  |
| **MySQL**            | Database storage                            |
| **SQL**              | Transaction analysis and fraud rules        |
| **Streamlit**        | Interactive dashboard                       |
| **Plotly**           | Data visualization                          |
| **Jupyter Notebook** | Development and testing                     |
| **GitHub**           | Project version control                     |

## 🔄 Project Workflow

```text
UPI Transaction Dataset
          ↓
    Data Cleaning
          ↓
      MySQL Database
          ↓
    Fraud Detection Rules
          ↓
      Risk Score
          ↓
      Risk Level
          ↓
   SQL-Based Analysis
          ↓
  Streamlit Dashboard
```

## 🚨 Fraud Detection Rules

The system assigns points according to predefined conditions.

| Condition                        | Risk Score |
| -------------------------------- | ---------: |
| Transaction amount > ₹50,000     |        +30 |
| Transaction between 12 AM – 5 AM |        +20 |
| Unknown device                   |        +20 |
| Public/Unknown network           |        +20 |
| Weekend transaction              |         +5 |

### Risk Classification

| Risk Score | Risk Level     |
| ---------: | -------------- |
|       0–29 | 🟢 Low Risk    |
|      30–59 | 🟡 Medium Risk |
|        60+ | 🔴 High Risk   |

## 📊 Dashboard Features

The Streamlit dashboard provides:

* 💳 Total transaction count
* 🚨 High-risk transaction count
* ⚠️ Medium-risk transaction count
* ✅ Low-risk transaction count
* 📊 Risk distribution visualization
* 📱 Device-wise transaction analysis
* 🌐 Network-wise transaction analysis
* 🕐 Hour-wise transaction activity
* 🚨 High-risk transaction table
* 🔍 Risk-level filtering
* 📋 Complete transaction data

## 🗄️ Database

The project uses a MySQL database named:

```text
upi_fraud
```

The main table is:

```text
transactions
```

Important fields include:

```text
transaction_id
timestamp
transaction_type
merchant_category
amount
transaction_status
sender_age_group
receiver_age_group
sender_state
sender_bank
receiver_bank
device_type
network_type
fraud_flag
hour_of_day
day_of_week
is_weekend
risk_score
risk_level
```

## 📁 Project Structure

```text
UPI-Transaction-and-Fraud-Detection/
│
├── dataset/
│   └── upi_transactions.csv
│
├── notebooks/
│   └── fraud_detection.ipynb
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

> File and folder names can be adjusted according to the final project structure.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Anushkasahu09/Upi-Transaction-and-Fraud-Detection-.git
```

### 2. Open the Project

```bash
cd Upi-Transaction-and-Fraud-Detection-
```

### 3. Install Required Libraries

```bash
pip install pandas mysql-connector-python streamlit plotly
```

### 4. Configure MySQL

Create the database:

```sql
CREATE DATABASE upi_fraud;
```

Create the `transactions` table and import the transaction dataset.

Update the MySQL connection details in the application:

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="upi_fraud"
)
```

Replace `YOUR_PASSWORD` with your local MySQL password.

## ▶️ Run the Dashboard

Start the Streamlit application using:

```bash
streamlit run app.py
```

The dashboard will open in your web browser.

## 📈 Future Scope

The project can be further improved by adding:

* Real-time UPI transaction monitoring
* Email/SMS fraud alerts
* More advanced fraud detection rules
* User authentication
* Transaction anomaly monitoring
* Geographic transaction analysis
* Bank-wise risk analysis
* Real-time database updates
* Machine Learning-based fraud detection as a future enhancement

## 🎓 Academic Purpose

This project was developed as an **MCA academic project** to demonstrate practical knowledge of:

* Python programming
* Data analysis
* SQL and database management
* Rule-based decision systems
* Data visualization
* Dashboard development

## 👩‍💻 Author

**Anushka Sahu**

MCA Student | Python | SQL | Data Analysis | Streamlit

---

⭐ If you find this project useful, consider giving the repository a star!
