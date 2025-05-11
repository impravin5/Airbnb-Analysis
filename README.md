# 🏡 Airbnb Data Analysis & Visualization

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit)
![Power BI](https://img.shields.io/badge/Visualization-Power%20BI-yellow?logo=powerbi)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-4ea94b?logo=mongodb)
![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)

This project provides an end-to-end solution for analyzing and visualizing Airbnb listing data using Python, MongoDB, Streamlit, and Power BI.

---

## 📁 Project Files

| File Name       | Description                                             |
|----------------|---------------------------------------------------------|
| `airb.py`       | Python script to launch the Streamlit web application  |
| `airbnb.pbix`   | Power BI dashboard for advanced visual analytics       |
| `README.md`     | Documentation for GitHub repository                    |

---

## 🚀 Features

- 🔍 Extracts Airbnb data from MongoDB Atlas
- 🧼 Cleans and transforms nested JSON data
- 📊 Interactive dashboards using Streamlit
- 🗺️ Geospatial visualizations using Plotly
- 📈 Advanced KPI and trend analysis with Power BI
- 🔧 Modular and scalable design

---

## 🧰 Tech Stack

- **Frontend:** Streamlit, Plotly, Matplotlib, Seaborn
- **Backend:** Python (Pandas, NumPy)
- **Database:** MongoDB Atlas (via `pymongo`)
- **Dashboard:** Power BI Desktop

---

## 📌 Application Pages

| Page Name                    | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `Home`                      | Project workflow, tools used, raw data sample                              |
| `Price Analysis`            | Price distributions, trends, outliers, scatterplots                        |
| `Availability Analysis`     | Room-type availability across 30, 60, 90, and 365 days                     |
| `Geospatial Visualizations` | Mapbox-based interactive scatter and density maps                          |
| `Location Based Visuals`    | Country-level analysis of price, property types, and minimum stays         |
| `Power BI Dashboard`        | Instructions and embedded insights from Power BI `.pbix` file              |
| `Conclusions`               | Final observations and recommendations                                     |

---

## 🔄 Workflow

### 1. **Data Extraction**
- Uses `pymongo` to fetch Airbnb data from MongoDB Atlas.
- Database: `sample_airbnb`, Collection: `listingsAndReviews`.

### 2. **Data Cleaning & Transformation**
- Extracts nested fields like location, host info, and reviews.
- Converts `Decimal128` to float, handles `NaN` values.
- Transforms data into a clean Pandas DataFrame.

### 3. **Exploratory Data Analysis**
- Distribution plots, histograms, scatter plots.
- Outlier detection and price correlation visualizations.

### 4. **Geospatial Mapping**
- Uses Plotly `scatter_mapbox` and `density_mapbox` for global listings.
- Offers filter options for color scale, size, and map style.

### 5. **Power BI Dashboard**
- Interactive `.pbix` dashboard available for deep-dive visual analysis.

---

## ▶️ How to Run

### ✅ Streamlit App
```bash
# Clone the repo
git clone https://github.com/your-username/airbnb-analysis.git
cd airbnb-analysis

# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run airb.py
