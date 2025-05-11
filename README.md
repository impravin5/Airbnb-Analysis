# 🏡 Airbnb Data Analysis & Visualization

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit)
![Power BI](https://img.shields.io/badge/Visualization-Power%20BI-yellow?logo=powerbi)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-4ea94b?logo=mongodb)
![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)

This project provides a full-stack, end-to-end solution for extracting, transforming, analyzing, and visualizing Airbnb listing data using **Python**, **MongoDB**, **Streamlit**, and **Power BI**. The dashboard reveals insights into pricing trends, availability patterns, host activity, and geospatial behavior.

---

## 📁 Project Structure

| File Name       | Description                                             |
|----------------|---------------------------------------------------------|
| `airb.py`       | Main Streamlit application with complete analytics     |
| `airbnb.pbix`   | Power BI dashboard with interactive insights           |
| `README.md`     | Documentation for this project                         |

---

## 🧰 Tech Stack & Tools

- **Frontend:** Streamlit, Plotly, Seaborn, Matplotlib
- **Backend/Data Handling:** Python, Pandas, NumPy, Regex
- **Database:** MongoDB Atlas (`pymongo`)
- **Dashboard Tool:** Power BI Desktop
- **Others:** Streamlit Option Menu, Pillow (image rendering)

---

## 🔄 Detailed Workflow (End-to-End Process)

### 🗃️ 1. Data Extraction from MongoDB Atlas

- **Tool:** `pymongo`
- Connects securely to MongoDB Atlas.
- Fetches all records from the `listingsAndReviews` collection in the `sample_airbnb` database.
- Handles nested documents such as location, amenities, and host info.

---

### 📊 2. Data Loading & Transformation

- **Libraries:** `pandas`, `numpy`, `bson.decimal128`
- Transforms raw MongoDB JSON into a clean tabular DataFrame.
- Extracts:
  - Property details (name, type, room type, amenities)
  - Geographical data (latitude, longitude, country)
  - Pricing (`price`, `cleaning_fee`, `security_deposit`)
  - Availability metrics and review scores.

---

### 🧼 3. Data Cleaning & Preprocessing

- Converts MongoDB’s `Decimal128` values to `float`.
- Handles missing values:
  - Fills numeric `NaN` with median.
  - Sets missing `security_deposit` to 0.
- Ensures correct data types using Pandas nullable `Int64` and float types.
- Processes deeply nested fields with `lambda` functions and `.get()` safely.

---

### 💻 4. Interactive EDA with Streamlit

- **Tool:** Streamlit
- Navigation via `streamlit_option_menu` in sidebar.
- Pages:
  - `Home`: Tool overview, raw data
  - `Price Analysis`: Price comparison by country/type
  - `Availability Analysis`: Days available over 30/60/90/365
  - `Geospatial Visuals`: Interactive Mapbox charts
  - `Location-Based`: Country-wise trends and types
  - `Power BI Dashboard`: Embedded link/screenshot
  - `Conclusions`: Summary of findings

---

### 📈 5. Visualizations

#### a. Price Analysis
- Average prices by **country** and **property type**
- Box plots for **price distribution** by room type
- Scatter plots:
  - Price vs. Minimum Nights
  - Price vs. Review Count

#### b. Availability Analysis
- Bar charts of **availability trends**
- Histogram for availability distribution
- Availability vs. Price scatter plot

#### c. Geospatial Visualizations
- **Scatter mapbox** for all listings globally
- **Density map** based on price or review score
- Customization: Color scale, marker size, map theme

#### d. Location-Based Analysis
- Area, Line, Bar, and Violin plots for:
  - Property type count
  - Minimum night stays
  - Country-level comparisons

---

### 📊 6. Power BI Dashboard

- File: `airbnb.pbix`
- Features:
  - Price trends
  - Booking frequency
  - Filters & slicers
  - Review sentiment correlations
- Can be previewed as an image or opened in Power BI Desktop.

---

### 📌 7. Insights & Conclusions

- Compare expensive vs. affordable room types and countries.
- Detect over/underbooked properties using availability patterns.
- Spot geographical hotspots of listings.
- Track how host ratings impact pricing.

---

# ✅ Key Outcomes and Insights

- Extracted and transformed complex Airbnb data from MongoDB Atlas using PyMongo and Pandas.
- Cleaned and normalized data including nested fields like coordinates, pricing, and host details.
- Identified countries with the highest average Airbnb listing prices.
- Highlighted top property types generating maximum revenue.
- Detected pricing outliers affecting overall market trends.
- Analyzed availability patterns across 30, 60, 90, and 365-day periods by room type.
- Found that entire homes have higher average availability than shared/private rooms.
- Visualized global listing density and pricing distribution using interactive Mapbox plots.
- Mapped high-demand regions with low availability for strategic market targeting.
- Compared country-wise differences in minimum night requirements.
- Showed top 10 property types by listing count across different countries.
- Created box plots to identify variability in stay durations by room type.
- Developed an interactive Power BI dashboard with filters, slicers, and trend analysis.
- Delivered visual insights into pricing behavior, review count, and room popularity.
- Helped identify optimal pricing strategies based on review performance.
- Empowered hosts to optimize listing details and improve booking potential.
- Equipped travelers with tools to explore the best-value destinations.
- Enabled data-driven decisions for stakeholders based on trends and location data.
- Combined Python, Streamlit, and Power BI to build a full-stack Airbnb analytics solution.


