import pandas as pd
from preswald import connect, get_df, text, slider, selectbox, plotly
import plotly.express as px

# Connect to our data sources. This makes sure everything defined in our config is ready to use.
connect()

# Load the video game sales dataset using the key 'games_csv'.
df = get_df("games_csv")

# Greet the user and provide a brief description of the dashboard.
text("# Video Game Sales Dashboard")
text("Welcome! Use the filters below to explore video game sales data.")

# Quick sanity check: Report how many records were loaded.
if df.empty:
    text("Uh oh, no data was loaded. Please check your CSV file and configuration.")
else:
    text(f"Dataset loaded successfully with {df.shape[0]} records.")

# For our filters to work properly, we need to ensure the 'Year' column is numeric.
if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
else:
    text("**Error:** 'Year' column missing in the CSV. Please fix your dataset.")

# Create sliders for choosing a release year range.
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_min_year = slider("Minimum Release Year", min_val=min_year, max_val=max_year, default=min_year)
selected_max_year = slider("Maximum Release Year", min_val=min_year, max_val=max_year, default=max_year)

# Add a dropdown to filter by Genre.
# We sort the list so the options appear in a reasonable order.
unique_genres = sorted(df["Genre"].dropna().unique())
genre_options = ["All"] + unique_genres  # "All" means no genre filtering.
selected_genre = selectbox("Select Genre", options=genre_options, default="All")

# Filter the dataset to include games within the chosen release year range.
filtered_df = df[(df["Year"] >= selected_min_year) & (df["Year"] <= selected_max_year)]

# Further filter by genre if a specific genre is selected.
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

# Let the user know how many records match their criteria.
text(f"Filtered dataset contains {filtered_df.shape[0]} records.")

# Visualization 1: Bar Chart for Total Global Sales by Platform.
# We group data by Platform and sum up the Global Sales.
platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().reset_index()

fig_bar = px.bar(
    platform_sales,
    x="Platform",
    y="Global_Sales",
    title="Total Global Sales by Platform (Filtered)",
    labels={"Global_Sales": "Global Sales (millions)"}
)
plotly(fig_bar)

# Visualization 2: Scatter Plot for Global Sales Over Time.
# This plot shows how global sales trend over the years, with points colored by Genre.
fig_scatter = px.scatter(
    filtered_df,
    x="Year",
    y="Global_Sales",
    color="Genre",
    hover_data=["Name", "Platform"],
    title="Global Sales Trend Over Time"
)
plotly(fig_scatter)

