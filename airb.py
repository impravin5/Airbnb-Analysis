import pandas as pd
import streamlit as st
import pymongo
from bson.decimal128 import Decimal128
from bson import Decimal128
import plotly.express as px
from PIL import Image

# Extract data from Mongppdb
client = pymongo.MongoClient(
    "mongodb+srv://pravinkumarm4010:pravin@pravin.dak9m.mongodb.net/?retryWrites=true&w=majority&appName=Pravin"
)
db = client["sample_airbnb"]
col = db["listingsAndReviews"]
data = col.find()
df = pd.DataFrame(data)

# Reset Index after Removing Duplicates
df.reset_index(drop=True, inplace=True)


# Reset Index after Removing Duplicates
df.reset_index(drop=True, inplace=True)

# Extract Required Columns Safely
data = pd.DataFrame(
    {
        "Id": df["_id"],
        "Name": df.get("name"),
        "Description": df.get("description"),
        "Country": df["address"].apply(lambda x: x.get("country", None)),
        "Longitude": df["address"].apply(
            lambda x: x.get("location", {}).get("coordinates", [None, None])[0]
        ),
        "Latitude": df["address"].apply(
            lambda x: x.get("location", {}).get("coordinates", [None, None])[1]
        ),
        "Property_Type": df.get("property_type"),
        "Room_Type": df.get("room_type"),
        "Bed_Type": df.get("bed_type"),
        "Amenities": df.get("amenities", []),
        "Minimum_Nights": df.get("minimum_nights"),
        "Maximum_Nights": df.get("maximum_nights"),
        "Cancellation_Policy": df.get("cancellation_policy"),
        "Cleaning_Fees": df.get("cleaning_fee"),
        "Price": df.get("price"),
        "Host_Id": df["host"].apply(lambda x: x.get("host_id", None)),
        "Host_Name": df["host"].apply(lambda x: x.get("host_name", None)),
        "Listing_URL": df.get("listing_url"),
        "Availability_30": df["availability"].apply(
            lambda x: x.get("availability_30", None)
        ),
        "Availability_60": df["availability"].apply(
            lambda x: x.get("availability_60", None)
        ),
        "Availability_90": df["availability"].apply(
            lambda x: x.get("availability_90", None)
        ),
        "Availability_365": df["availability"].apply(
            lambda x: x.get("availability_365", None)
        ),
        "Security_deposit": df.get("security_deposit"),
        "Number_of_Reviews": df.get("number_of_reviews"),
        "Review_Count": df["review_scores"].apply(
            lambda x: x.get("review_scores_rating", 0) if isinstance(x, dict) else 0
        ),
        "Review_Score": df["review_scores"].apply(
            lambda x: x.get("review_scores_value", 0) if isinstance(x, dict) else 0
        ),
    }
)

# Data Cleaning
# Data Preparation
df = data.copy()
numeric_cols = [
    "Availability_30",
    "Minimum_Nights",
    "Maximum_Nights",
    "Availability_60",
    "Availability_90",
    "Availability_365",
    "Number_of_Reviews",
    "Review_Count",
    "Review_Score",
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="raise").astype("Int64")  # 'Int64' supports NaN values

# Convert Decimal128 to float safely
df["Price"] = df["Price"].apply(
    lambda x: float(str(x)) if isinstance(x, Decimal128) else x
)
df["Cleaning_Fees"] = df["Cleaning_Fees"].apply(
    lambda x: float(str(x)) if isinstance(x, Decimal128) else x
)

# Fill NaN with median and convert to Int64
df["Price"] = df["Price"].fillna(df["Price"].median()).astype("Int64")
df["Cleaning_Fees"] = df["Cleaning_Fees"].fillna(df["Cleaning_Fees"].median()).astype(
    "Int64"
)
df["Security_deposit"] = df["Security_deposit"].apply(
    lambda x: float(str(x)) if isinstance(x, Decimal128) else x
)
# Fill NaN with 0
df["Security_deposit"] = df["Security_deposit"].fillna(0)
# convert to int
df["Security_deposit"] = pd.to_numeric(df["Security_deposit"], errors="coerce").astype(
    "Int64"
)


# Front Page Design
selected_page = st.sidebar.radio(
    "**Select a Page**",
    [
        "Home",
        "Price Analysis",
        "Availability Analysis",
        "Geospatial Visualizations",
        "Location Based Visualizations",
        "Power BI Dashboard",
        "Conclusions",
    ],
)

if selected_page == "Home":
    st.title("Airbnb Analysis & Visualizations")
    st.markdown("---")
    st.header("Application Workflow and Tools ")
    st.markdown(
        "This application provides a comprehensive analysis of Airbnb data. Here's a breakdown of the processing steps and tools used:"
    )
    with st.expander("**1. Data Extraction from MongoDB Atlas**"):
        st.markdown(
            """
            * **Tool:** `pymongo` library.
            * **Reason:** Used to connect to and interact with MongoDB databases. It allows fetching data from the MongoDB Atlas cloud service.
            * **Process:** Establishes a connection to the 'sample_airbnb' database and retrieves all documents from the 'listingsAndReviews' collection.
            """
        )
    with st.expander("**2. Initial DataFrame Creation and Handling**"):
        st.markdown(
            """
            * **Tool:** `pandas` library.
            * **Reason:** Essential for data manipulation and analysis in Python. Provides DataFrames, which are tabular data structures.
            * **Process:** Converts the MongoDB data into a Pandas DataFrame for easier handling. The index is reset to ensure proper data alignment.
            """
        )
    with st.expander("**3. Data Extraction and Transformation**"):
        st.markdown(
            """
            * **Tool:** `pandas` library, lambda functions.
            * **Reason:** `pandas` is used for creating a structured DataFrame with relevant columns. Lambda functions provide a concise way to extract nested data. The `.get()` method ensures safe access to potentially missing keys.
            * **Process:** A new DataFrame is created by selecting and transforming specific columns, including handling nested structures within the 'address' and 'host' fields to extract information like 'Country', 'Longitude', 'Latitude', 'Host ID', and 'Host Name'.
            """
        )
    with st.expander("**4. Data Cleaning and Preparation**"):
        st.markdown(
            """
            * **Tool:** `pandas` library, `numpy` (implicitly through `pandas`).
            * **Reason:** `pandas` is used for data type conversion, handling missing values (NaN), and imputation. `numpy`'s `NaN` representation is used by `pandas`.
            * **Process:**
                * Converts relevant columns to appropriate numeric types (`Int64` to handle missing integers).
                * Safely converts MongoDB's `Decimal128` format to Python floats for compatibility with analysis and visualization libraries.
                * Imputes missing 'Price' and 'Cleaning_Fees' using the median to provide a central tendency for missing values without significantly skewing the distribution.
                * Fills missing 'Security_deposit' values with 0, assuming no deposit if the information is absent.
            """
        )
    st.header("Streamlit Application Pages ")
    st.markdown(
        """
        The application is structured into several interactive pages accessible through the sidebar:

        * **Home:** Provides an overview of the application, its workflow, and the tools used (this page).
        * **Price Analysis:** Allows users to explore price distributions and averages based on various filters.
        * **Availability Analysis:** Enables the visualization of property availability across different timeframes and room types.
        * **Geospatial Visualizations:** Displays interactive maps showing the geographical distribution of listings.
        * **Location Based Visualizations:** Presents comparisons of prices and property types across different locations.
        * **Conclusions:** Summarizes the key findings and insights derived from the analysis.
        """
    )
    st.markdown("---")
    st.subheader("Raw Data Sample")
    st.write(df)
    st.subheader("Data Types")
    st.write(df.dtypes)



elif selected_page == "Price Analysis":
    st.title("Airbnb Price Analysis")
    st.markdown("---")

    if not df.empty:
        st.header("Price Variation Analysis")

        st.subheader("Average Price by Country")
        country_price_df = df.groupby('Country')['Price'].mean().reset_index()
        fig_price_by_country = px.bar(country_price_df, x='Country', y='Price',
                                        title="Average Price by Country",
                                        labels={'Price': 'Average Price'})
        st.plotly_chart(fig_price_by_country)
        st.markdown("*Potential Problem:* Countries with very few listings might skew averages.")
        st.markdown("*How to Overcome:* Consider filtering out countries with a low number of data points.")

        st.subheader("Average Price by Property Type (Top 15)")
        property_price_df = df.groupby('Property_Type')['Price'].mean().reset_index()
        property_price_df = property_price_df.sort_values(by='Price', ascending=False).head(15)
        fig_price_by_property = px.bar(property_price_df, x='Property_Type', y='Price',
                                         title="Average Price by Property Type (Top 15)",
                                         labels={'Price': 'Average Price'})
        st.plotly_chart(fig_price_by_property)
        st.markdown("*Potential Problem:* 'Other' or less frequent property types might have high variance.")
        st.markdown("*How to Overcome:* Group less frequent types or focus on the most common ones.")

        st.subheader("Price Distribution by Room Type")
        fig_price_by_room = px.box(df, x='Room_Type', y='Price', color='Room_Type',
                                    title="Price Distribution by Room Type",
                                    labels={'Price': 'Price'})
        st.plotly_chart(fig_price_by_room)
        st.markdown("*Potential Problem:* Box plots can hide the exact distribution of prices.")
        st.markdown("*How to Overcome:* Supplement with histograms for a more detailed view.")

        st.subheader("Price Outliers")
        fig_price_outliers = px.box(df, y='Price', title="Price Outliers")
        st.plotly_chart(fig_price_outliers)
        st.markdown("*Potential Problem:* Outliers can skew the perception of typical prices.")
        st.markdown("*How to Overcome:* Consider investigating and potentially removing extreme outliers for some analyses.")

        st.subheader("Price vs. Minimum Nights")
        fig_price_vs_min_nights = px.scatter(df, x='Minimum_Nights', y='Price',
                                            title="Price vs. Minimum Nights",
                                            labels={'Price': 'Price', 'Minimum_Nights': 'Minimum Nights'})
        st.plotly_chart(fig_price_vs_min_nights)
        st.markdown("*Potential Problem:* Many listings might have very low minimum nights, clustering the data.")
        st.markdown("*How to Overcome:* Consider filtering the data to a reasonable range of minimum nights for better visibility.")

        st.subheader("Price vs. Number of Reviews")
        fig_price_vs_num_reviews = px.scatter(df, x='Number_of_Reviews', y='Price',
                                            title="Price vs. Number of Reviews",
                                            labels={'Price': 'Price', 'Number_of_Reviews': 'Number of Reviews'})
        st.plotly_chart(fig_price_vs_num_reviews)
        st.markdown("*Potential Problem:* The majority of listings might have a low number of reviews.")
        st.markdown("*How to Overcome:* Consider binning the number of reviews or using a logarithmic scale for the x-axis.")

    else:
        st.info("No data available based on the selected filters.")

elif selected_page == "Availability Analysis":
    st.title("Availability Analysis")
    st.markdown("---")

    if not df.empty:
        st.subheader("Average Availability by Room Type")

        col1, col2 = st.columns(2)
        with col1:
            avg_availability_30 = (
                df.groupby("Room_Type")["Availability_30"].mean().reset_index()
            )
            avg_availability_30.rename(
                columns={"Room_Type": "Room_Type"}, inplace=True
            )
            fig_avail_30 = px.bar(
                avg_availability_30,
                x="Room_Type",
                y="Availability_30",
                title="Average Availability (Next 30 Days)",
                labels={"Availability_30": "Average Days Available"},
                color="Room_Type",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_avail_30)
            st.markdown("*Potential Problem:* Averages don't show the distribution of availability.")
            st.markdown("*How to Overcome:* Look at the availability histograms for more detail.")

            avg_availability_90 = (
                df.groupby("Room_Type")["Availability_90"].mean().reset_index()
            )
            avg_availability_90.rename(
                columns={"Room_Type": "Room_Type"}, inplace=True
            )
            fig_avail_90 = px.bar(
                avg_availability_90,
                x="Room_Type",
                y="Availability_90",
                title="Average Availability (Next 90 Days)",
                labels={"Availability_90": "Average Days Available"},
                color="Room_Type",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            st.plotly_chart(fig_avail_90)
            st.markdown("*Potential Problem:* Long-term averages can mask short-term trends.")
            st.markdown("*How to Overcome:* Compare with shorter-term availability metrics.")

        with col2:
            avg_availability_60 = (
                df.groupby("Room_Type")["Availability_60"].mean().reset_index()
            )
            avg_availability_60.rename(
                columns={"Room_type": "Room_Type"}, inplace=True
            )
            fig_avail_60 = px.bar(
                avg_availability_60,
                x="Room_Type",
                y="Availability_60",
                title="Average Availability (Next 60 Days)",
                labels={"Availability_60": "Average Days Available"},
                color="Room_Type",
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            st.plotly_chart(fig_avail_60)
            st.markdown("*Potential Problem:* Different room types have varying numbers of listings.")
            st.markdown("*How to Overcome:* Consider the number of listings when interpreting averages.")

            avg_availability_365 = (
                df.groupby("Room_Type")["Availability_365"].mean().reset_index()
            )
            avg_availability_365.rename(
                columns={"Room_type": "Room_Type"}, inplace=True
            )
            fig_avail_365 = px.bar(
                avg_availability_365,
                x="Room_Type",
                y="Availability_365",
                title="Average Availability (Next 365 Days)",
                labels={"Availability_365": "Average Days Available"},
                color="Room_Type",
                color_discrete_sequence=px.colors.qualitative.Dark2,
            )
            st.plotly_chart(fig_avail_365)
            st.markdown("*Potential Problem:* High average availability might indicate lower demand.")
            st.markdown("*How to Overcome:* Correlate with price and other factors.")

        st.markdown("---")

        st.subheader("Distribution of Availability (Next 30 Days)")
        fig_hist_30 = px.histogram(
            df,
            x="Availability_30",
            color="Room_Type",
            title="Distribution of Availability (Next 30 Days)",
            labels={"Availability_30": "Days Available"},
            marginal='rug'
        )
        st.plotly_chart(fig_hist_30)
        st.markdown("*Potential Problem:* Histograms are sensitive to the number of bins.")
        st.markdown("*How to Overcome:* Experiment with different bin sizes to see the underlying shape.")

        st.subheader("Availability (Next 30 Days) vs. Price")
        fig_avail_30_vs_price = px.scatter(df, x='Availability_30', y='Price',
                                            title="Availability (Next 30 Days) vs. Price",
                                            labels={'Price': 'Price', 'Availability_30': 'Days Available'})
        st.plotly_chart(fig_avail_30_vs_price)
        st.markdown("*Potential Problem:* The relationship between price and availability might not be linear.")
        st.markdown("*How to Overcome:* Look for general trends or clusters rather than strict correlations.")

    else:
        None

elif selected_page == "Geospatial Visualizations":
    st.title("Geospatial Visualizations")
    if "Latitude" in df.columns and "Longitude" in df.columns:
        st.subheader("Interactive Map Controls")

        # Options for Color
        color_options = ["Price", "Review_Count", "Review_Score", "Number_of_Reviews"]
        color_column = st.selectbox("Color by:", color_options, index=0)  # Default to 'Price'

        # Size Option (optional)
        size_options = ["Price", "Review_Count", "Number_of_Reviews", None]
        size_column = st.selectbox("Size by:", size_options, index=0)  # Default to 'Price', None option

        # Color Scale Selection
        color_scales = px.colors.named_colorscales()
        selected_color_scale = st.selectbox("Color Scale:", color_scales, index=color_scales.index("viridis"))  # Default to 'viridis'

        # Map Style Selection
        map_styles = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner", "stamen-watercolor"]
        selected_map_style = st.selectbox("Map Style:", map_styles, index=0)  # Default to 'open-street-map'

        st.markdown("---")
        st.subheader("Airbnb Listings on Full Map")
        fig_scatter_geo = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            color=color_column,
            size=size_column if size_column else None,
            hover_name="Name",
            color_continuous_scale=selected_color_scale,
            size_max=15,
            zoom=0.5,  # Set initial zoom level to show the full world
            height=700, # Increase height for better view
            title=f"Airbnb Listings colored by {color_column} and sized by {size_column if size_column else 'Price'}",
        )
        fig_scatter_geo.update_layout(mapbox_style=selected_map_style)
        fig_scatter_geo.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        st.plotly_chart(fig_scatter_geo, use_container_width=True) # Ensure it uses full container width
        st.markdown("*Potential Problem:* Overlapping markers can make it hard to see individual listings in dense areas.")
        st.markdown("*How to Overcome:* Zoom in on specific regions or consider using a clustering approach or a heatmap.")

        st.markdown("---")
        st.subheader("Listing Density Heatmap on Full Map")
        heatmap_color_scale = st.selectbox("Heatmap Color Scale:", color_scales, index=color_scales.index("plasma"))  # Default to 'plasma'
        fig_density_geo = px.density_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            z="Price",  # Using Price for density intensity as an example
            radius=10,
            center=dict(lat=df["Latitude"].mean(), lon=df["Longitude"].mean()),
            zoom=0.5,    # Set initial zoom level to show the full world
            mapbox_style=selected_map_style,
            height=700,  # Increase height for better view
            title="Density of Airbnb Listings (Intensity based on Price)",
            color_continuous_scale=heatmap_color_scale,
        )
        fig_density_geo.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        st.plotly_chart(fig_density_geo, use_container_width=True) # Ensure it uses full container width
        st.markdown("*Potential Problem:* The chosen radius can significantly impact the appearance of the heatmap.")
        st.markdown("*How to Overcome:* Experiment with different radius values to find the most informative visualization.")

    else:
        st.info(
            "Latitude and longitude data are not available for geospatial visualization. Please check your data.")            

elif selected_page == "Location Based Visualizations":
    st.title("Location Based Visualizations")
    # Average Price by Country (Bar Chart)
    st.subheader("Average Price by Country")
    country_avg_price_df = df.groupby("Country", as_index=False)["Price"].mean()
    fig_country_price = px.area(
        country_avg_price_df,
        x="Country",
        y="Price",
        title="Average Price by Country",
        labels={"Price": "Average Price"},
    )
    fig_country_price.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_country_price)
    st.markdown("*Potential Problem:* Average price can be influenced by the number of listings per country.")
    st.markdown("*How to Overcome:* Consider the number of listings when comparing averages.")

    # Top 10 Property Types by Count
    st.subheader("Top 10 Property Types by Listing Count")
    property_type_counts = df["Property_Type"].value_counts().head(10).reset_index()
    property_type_counts.columns = ["Property_Type", "Count"]  # Rename columns for clarity

    fig_top_10_property_types = px.bar(
        property_type_counts,
        x="Property_Type",
        y="Count",
        title="Top 10 Property Types by Listing Count",
        labels={"Count": "Number of Listings", "Property_Type": "Property Type"},
    )
    fig_top_10_property_types.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top_10_property_types)
    st.markdown("*Potential Problem:* Focusing on the top 10 might hide other significant property types.")
    st.markdown("*How to Overcome:* Consider analyzing the distribution of all property types.")

    st.subheader("Distribution of Minimum Nights by Room Type")
    fig_min_nights_by_room = px.box(df, x='Room_Type', y='Minimum_Nights', color='Room_Type',
                                    title="Distribution of Minimum Nights by Room Type",
                                    labels={'Minimum_Nights': 'Minimum Nights'})
    st.plotly_chart(fig_min_nights_by_room)
    st.markdown("*Potential Problem:* The scale of minimum nights can vary greatly.")
    st.markdown("*How to Overcome:* Consider filtering out extreme values if necessary to focus on the typical range.")

    st.subheader("Average Minimum Nights by Country")
    country_min_nights_df = df.groupby("Country", as_index=False)["Minimum_Nights"].mean()
    fig_country_min_nights = px.line(
        country_min_nights_df,
        x="Country",
        y="Minimum_Nights",
        title="Average Minimum Nights by Country",
        labels={"Minimum_Nights": "Average Minimum Nights"},
    )
    fig_country_min_nights.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_country_min_nights)
    st.markdown("*Potential Problem:* Countries with different tourism patterns might show varying minimum night stays.")
    st.markdown("*How to Overcome:* Consider the context of travel norms in each country.")


    st.subheader("Distribution of Property Types by Country (Top 10)")
    property_country_counts = df.groupby('Country')['Property_Type'].value_counts().nlargest(10).reset_index(name='Count')
    fig_property_by_country = px.violin (property_country_counts, x='Country', y='Count', color='Property_Type',
                                    title="Top 10 Property Types by Country",
                                    labels={'Count': 'Number of Listings', 'Property_Type': 'Property Type'})
    st.plotly_chart(fig_property_by_country)
    st.markdown("*Potential Problem:* Countries with many listings might dominate the top property types.")
    st.markdown("*How to Overcome:* Consider normalizing the counts by the total number of listings in each country.")

elif selected_page == "Power BI Dashboard":
    st.title("Power BI Dashboard")
    st.markdown("---")
    st.subheader("Access the Interactive Dashboard")

    # Option 1: Display a link
    power_bi_dashboard_url = "YOUR_POWER_BI_DASHBOARD_LINK_HERE"
    st.markdown(f"You can access the interactive Power BI dashboard with more detailed insights here: [Power BI Dashboard]({power_bi_dashboard_url})")

    # Option 2: Display a static image (if you have one)
    try:
         image = Image.open("powerbi Dashboard.png")
         st.image(image, caption="Preview of the Power BI Dashboard", use_column_width=True)
    except FileNotFoundError:
         st.warning("Power BI Dashboard screenshot not found.")

    # Option 3: Display a summary of insights
    st.markdown("---")
    st.subheader("Key Insights in the Power BI Dashboard:")
    st.markdown("""
    * Explore detailed trends in average prices across different neighborhoods.
    * Analyze booking patterns and occupancy rates over various time periods.
    * Identify key factors influencing listing prices based on advanced statistical analysis.
    * Visualize review sentiment and its correlation with other listing attributes.
    """)

    # Option 4: Instructions for access (if needed)
    st.markdown("---")
    st.subheader("How to Access the Power BI Dashboard:")
    st.markdown("""
    1.  Open your web browser and navigate to [YOUR_POWER_BI_URL_OR_PORTAL].
    2.  Log in using your organizational credentials.
    3.  Locate the dashboard named 'Airbnb Analysis Dashboard'.
    """)

elif selected_page == "Conclusions":
    st.title("Conclusions")
    st.markdown(
        """
        ## Key Outcomes and Insights:

        * **Comprehensive Airbnb Data Overview:** The dashboard provides a holistic view of Airbnb data, consolidating information into an easily digestible format.
        * **Price Trend Analysis:**
            * You can effectively analyze price variations based on property type and location.
            * Identify the most and least expensive property types.
            * Understand how average prices differ across countries.
        * **Availability Patterns:**
            * Gain insights into property availability trends over different timeframes (30, 60, 90, and 365 days).
            * Compare average availability across various room types.
        * **Geospatial Analysis:**
            * Visualize listing locations on an interactive map.
            * Identify areas with a high concentration of listings.
        * **Location-Based Insights:**
            * Compare average prices across different countries.
            * Identify the most common property types.
        * **Data-Driven Decision Making:** The dashboard empowers users to make informed decisions related to:
            * Understanding market dynamics for travelers and hosts.
            * Identifying potential areas of interest.

        In essence, this dashboard serves as a valuable tool for anyone looking to understand Airbnb market trends and property dynamics.
        """
    )
