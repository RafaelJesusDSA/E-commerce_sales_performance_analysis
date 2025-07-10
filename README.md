# Olist E-commerce Performance Dashboard

## Overview
This project provides a comprehensive analysis of the Olist E-commerce public dataset. It focuses on extracting key sales performance indicators (KPIs) and visualizing data to provide actionable insights into sales trends, customer behavior, and operational efficiency within the e-commerce platform. The analysis leverages Python for robust data preparation and Power BI Desktop for interactive dashboard visualization.

## Objectives
* Calculate and visualize key performance indicators (KPIs) for sales and operational performance.
* Analyze total revenue distribution by customer state to identify key markets.
* Understand the overall distribution of order statuses to evaluate fulfillment efficiency.
* Explore the relationship between item price and freight cost to identify potential cost drivers or pricing strategies.

## Data Source
The data utilized in this project is the [Olist E-commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). This dataset, available on Kaggle, contains information on 100k orders made at Olist Store, encompassing various entities like customers, orders, order items, products, sellers, and geolocation data.

**Disclaimer:** Data sourced from Olist E-commerce Dataset (2016-2018), utilized for academic study focusing on historical e-commerce operational patterns.

## Tools & Technologies
* **Python:** Used for data cleaning, transformation, and initial KPI calculation using libraries such as `pandas`.
* **Power BI Desktop:** Utilized for data modeling, creating DAX measures, and designing the interactive dashboard visualizations.

## Key Performance Indicators (KPIs)
* **Revenue:** Total sales revenue generated.
* **Avg. Ticket:** Average revenue per order.
* **Orders:** Total number of unique orders placed.
* **Products:** Total number of individual products (items) sold.
* **Customers:** Total number of unique customers.
* **Avg. Items:** Average number of items per order.
* **Avg. Freight:** Average freight value per item.

## Dashboard Preview
Here's a preview of the interactive dashboard created in Power BI:

![Olist E-commerce Performance Dashboard](reports/dashboard_overview.png)
*(Ensure the path `reports/dashboard_overview.png` matches the actual location and filename of your dashboard image)*

## Project Structure

e-commerce_sales_performance_analysis/  # Main project directory
├── data/                  # Contains raw CSV data files and the processed data (e-commerce_data_processed.csv)
├── scripts/               # Contains Python scripts for data preparation and initial KPI calculations
├── reports/               # Stores the Power BI Desktop file (.pbix), exported PDF, and dashboard PNG images
├── README.md              # Project overview, documentation, and usage instructions
└── .gitignore             # Specifies intentionally untracked files to ignore from Git version control

## How to Use
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR_GITHUB_USERNAME]/e-commerce_sales_performance_analysis.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd e-commerce_sales_performance_analysis
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *You may need to create a `requirements.txt` file listing all Python libraries used in `data_preparation_and_kpi_calculation.py` (e.g., `pandas`).*
4.  **Run the data preparation script:**
    ```bash
    python scripts/data_preparation_and_kpi_calculation.py
    ```
    *This script will process the raw CSV files and generate `e-commerce_data_processed.csv` in the `data/` folder.*
5.  **Open the Power BI Dashboard:**
    *Open the `reports/Projeto_Ecommerce_KPIs.pbix` file using Power BI Desktop.*
6.  **Refresh Data:**
    *If prompted or if changes were made to the processed data, refresh the data sources within Power BI to ensure the latest data is loaded into the dashboard.*

---
*Developed by Rafael Jesus*
*Connect with me on [LinkedIn](https://www.linkedin.com/in/rafaeljesus-)*
*Contact: rafael.sanjes@hotmail.com *


