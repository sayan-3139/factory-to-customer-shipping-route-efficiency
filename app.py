import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned shipping dataset
shipping_df = pd.read_csv("Nassau_Candy_Cleaned.csv")

# Factory mapping based on Product Name
product_factory = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

shipping_df["Factory"] = shipping_df["Product Name"].map(product_factory)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Nassau Candy Shipping Analytics",
    page_icon="📦",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
kpi_df = pd.read_csv("Route_Efficiency_KPI.csv")
df = pd.read_csv("Nassau_Candy_Cleaned.csv")

product_factory = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(product_factory)

# -----------------------------
# Dashboard Header
# -----------------------------
st.title("📦 Factory-to-Customer Shipping Route Efficiency")
st.subheader("Nassau Candy Distributor")

st.markdown("---")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

# Factory filter
factory_options = ["All"] + sorted(kpi_df["Factory"].unique().tolist())

selected_factory = st.sidebar.selectbox(
    "Select Factory",
    factory_options,
    key="factory_filter"
)

# State/Province filter
if selected_factory == "All":
    state_options = ["All"] + sorted(
        kpi_df["State/Province"].unique().tolist()
    )
else:
    state_options = ["All"] + sorted(
        kpi_df.loc[
            kpi_df["Factory"] == selected_factory,
            "State/Province"
        ].unique().tolist()
    )

selected_state = st.sidebar.selectbox(
    "Select State/Province",
    state_options,
    key="state_filter"
)

# Ship Mode filter
ship_mode_options = ["All"] + sorted(df["Ship Mode"].dropna().unique().tolist())

selected_ship_mode = st.sidebar.selectbox(
    "Select Ship Mode",
    ship_mode_options
)

# Date Range Filter
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Minimum shipment volume
min_shipments = st.sidebar.slider(
    "Minimum Shipments",
    min_value=0,
    max_value=int(kpi_df["Total_Shipments"].max()),
    value=0,
    step=10
)

# -----------------------------
# Apply Filters
# -----------------------------

filtered_source = df.copy()

# Apply Order Date filter
if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_source = filtered_source[
        (filtered_source["Order Date"].dt.date >= start_date) &
        (filtered_source["Order Date"].dt.date <= end_date)
    ]

# Apply Factory filter
if selected_factory != "All":
    filtered_source = filtered_source[
        filtered_source["Factory"] == selected_factory
    ]

# Apply State/Province filter
if selected_state != "All":
    filtered_source = filtered_source[
        filtered_source["State/Province"] == selected_state
    ]

# Recalculate route KPIs after filtering
filtered_df = (
    filtered_source
    .groupby(["Factory", "State/Province"])
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std")
    )
    .reset_index()
)

# Calculate delay frequency
overall_avg_lead = filtered_source["Shipping Lead Time"].mean()

filtered_source["Delayed"] = (
    filtered_source["Shipping Lead Time"] > overall_avg_lead
)

delay_rate = (
    filtered_source
    .groupby(["Factory", "State/Province"])["Delayed"]
    .mean()
    .reset_index(name="Delay_Frequency_Percent")
)

delay_rate["Delay_Frequency_Percent"] *= 100

filtered_df = filtered_df.merge(
    delay_rate,
    on=["Factory", "State/Province"],
    how="left"
)

# Route Efficiency Score
filtered_df["Route_Efficiency_Score"] = (
    100000 / filtered_df["Average_Lead_Time"]
)

# Apply minimum shipment filter
filtered_df = filtered_df[
    filtered_df["Total_Shipments"] >= min_shipments
]

# Apply Ship Mode filter
if selected_ship_mode != "All":

    # Filter original shipment data by selected ship mode
    mode_df = df[df["Ship Mode"] == selected_ship_mode].copy()

    # Calculate delay using overall average lead time
    overall_avg_lead = df["Shipping Lead Time"].mean()
    mode_df["Delayed"] = (
        mode_df["Shipping Lead Time"] > overall_avg_lead
    )

    # Recalculate route KPIs for the selected ship mode
    ship_mode_routes = (
        mode_df.groupby(["Factory", "State/Province"])
        .agg(
            Total_Shipments=("Order ID", "count"),
            Average_Lead_Time=("Shipping Lead Time", "mean"),
            Lead_Time_Variability=("Shipping Lead Time", "std"),
            Delay_Frequency_Percent=("Delayed", "mean")
        )
        .reset_index()
    )

    ship_mode_routes["Delay_Frequency_Percent"] *= 100

    # Calculate custom Route Efficiency Score
    ship_mode_routes["Route_Efficiency_Score"] = (
        (100 / ship_mode_routes["Average_Lead_Time"]) * 1000
    )

    # Remove missing variability values
    ship_mode_routes["Lead_Time_Variability"] = (
        ship_mode_routes["Lead_Time_Variability"].fillna(0)
    )

    # Use the recalculated values
    filtered_df = ship_mode_routes.copy()

# -----------------------------
# KPI Calculations
# -----------------------------
if len(filtered_df) > 0:

    total_shipments = filtered_df["Total_Shipments"].sum()

    average_lead_time = (
        (
            filtered_df["Average_Lead_Time"]
            * filtered_df["Total_Shipments"]
        ).sum()
        / total_shipments
    )

    average_delay_frequency = (
        (
            filtered_df["Delay_Frequency_Percent"]
            * filtered_df["Total_Shipments"]
        ).sum()
        / total_shipments
    )

    average_efficiency_score = (
        (
            filtered_df["Route_Efficiency_Score"]
            * filtered_df["Total_Shipments"]
        ).sum()
        / total_shipments
    )

else:
    total_shipments = 0
    average_lead_time = 0
    average_delay_frequency = 0
    average_efficiency_score = 0

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Total Shipments",
        f"{total_shipments:,.0f}"
    )

with col2:
    st.metric(
        "⏱️ Average Lead Time",
        f"{average_lead_time:,.1f} days"
    )

with col3:
    st.metric(
        "⚠️ Delay Frequency",
        f"{average_delay_frequency:.1f}%"
    )

with col4:
    st.metric(
        "🎯 Route Efficiency Score",
        f"{average_efficiency_score:.2f}"
    )

st.markdown("---")

# -----------------------------
# Route Efficiency KPI Dataset
# -----------------------------
st.header("📊 Route Efficiency KPI Dataset")

st.write(
    f"Showing **{len(filtered_df)} routes** based on selected filters."
)

st.dataframe(
    filtered_df,
    width="stretch"
)

# -----------------------------
# Route Efficiency Overview
# -----------------------------
st.header("📈 Route Efficiency Overview")

factory_summary = (
    filtered_df
    .groupby("Factory")
    .agg(
        Average_Lead_Time=("Average_Lead_Time", "mean"),
        Total_Shipments=("Total_Shipments", "sum")
    )
    .reset_index()
)

fig_factory = px.bar(
    factory_summary,
    x="Factory",
    y="Average_Lead_Time",
    title="Average Lead Time by Factory",
    labels={
        "Factory": "Factory",
        "Average_Lead_Time": "Average Lead Time (Days)"
    },
    text_auto=".1f"
)

fig_factory.update_layout(
    xaxis_title="Factory",
    yaxis_title="Average Lead Time (Days)"
)

st.plotly_chart(
    fig_factory,
    width="stretch"
)

# -----------------------------
# Top 10 and Bottom 10 Routes
# -----------------------------

st.header("🏆 Route Performance Ranking")

# Create route name
filtered_df["Route"] = (
    filtered_df["Factory"]
    + " → "
    + filtered_df["State/Province"]
)

# Top 10 fastest routes
top_10_routes = (
    filtered_df
    .sort_values("Average_Lead_Time", ascending=True)
    .head(10)
)

fig_top = px.bar(
    top_10_routes.sort_values("Average_Lead_Time"),
    x="Average_Lead_Time",
    y="Route",
    orientation="h",
    title="🏆 Top 10 Most Efficient Routes",
    labels={
        "Average_Lead_Time": "Average Lead Time (Days)",
        "Route": "Factory → Customer State"
    },
    text_auto=".1f"
)

st.plotly_chart(
    fig_top,
    width="stretch"
)

# Bottom 10 slowest routes
bottom_10_routes = (
    filtered_df
    .sort_values("Average_Lead_Time", ascending=False)
    .head(10)
)

fig_bottom = px.bar(
    bottom_10_routes.sort_values("Average_Lead_Time"),
    x="Average_Lead_Time",
    y="Route",
    orientation="h",
    title="⚠️ Bottom 10 Least Efficient Routes",
    labels={
        "Average_Lead_Time": "Average Lead Time (Days)",
        "Route": "Factory → Customer State"
    },
    text_auto=".1f"
)

st.plotly_chart(
    fig_bottom,
    width="stretch"
)

# --------------------------------
# Geographic Shipping Map
# --------------------------------
st.markdown("---")
st.header("🗺️ Geographic Shipping Map")

# US state abbreviations
state_codes = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
    "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

# State-level shipping performance
geo_df = (
    filtered_df.groupby("State/Province")
    .agg(
        Total_Shipments=("Total_Shipments", "sum"),
        Average_Lead_Time=("Average_Lead_Time", "mean"),
        Delay_Frequency=("Delay_Frequency_Percent", "mean")
    )
    .reset_index()
)

geo_df["State Code"] = geo_df["State/Province"].map(state_codes)

# Keep only US states for the US map
us_geo_df = geo_df.dropna(subset=["State Code"]).copy()

fig_map = px.choropleth(
    us_geo_df,
    locations="State Code",
    locationmode="USA-states",
    color="Average_Lead_Time",
    scope="usa",
    hover_name="State/Province",
    hover_data={
        "State Code": False,
        "Total_Shipments": True,
        "Average_Lead_Time": ":.1f",
        "Delay_Frequency": ":.1f"
    },
    color_continuous_scale="RdYlGn_r",
    labels={
        "Average_Lead_Time": "Avg Lead Time (Days)",
        "Total_Shipments": "Shipments",
        "Delay_Frequency": "Delay Frequency (%)"
    },
    title="US Shipping Efficiency Heatmap"
)

fig_map.update_layout(
    height=600
)

st.plotly_chart(fig_map, width="stretch")


# --------------------------------
# Regional Bottleneck Visualization
# --------------------------------
st.subheader("🚧 Regional Bottleneck Analysis")

regional_df = (
    df.groupby("Region")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
       Delay_Frequency=("Shipping Lead Time", lambda x: (x > df["Shipping Lead Time"].mean()).mean())
    )
    .reset_index()
)

regional_df["Delay_Frequency"] = regional_df["Delay_Frequency"] * 100

fig_region = px.bar(
    regional_df.sort_values("Average_Lead_Time", ascending=False),
    x="Region",
    y="Average_Lead_Time",
    text="Average_Lead_Time",
    hover_data=[
        "Total_Shipments",
        "Delay_Frequency"
    ],
    labels={
        "Average_Lead_Time": "Average Lead Time (Days)",
        "Region": "Customer Region"
    },
    title="Average Shipping Lead Time by Region"
)

fig_region.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

fig_region.update_layout(height=450)

st.plotly_chart(fig_region, width="stretch")

# -----------------------------
# Ship Mode Comparison
# -----------------------------
st.header("🚚 Ship Mode Comparison")

ship_mode_summary = (
    shipping_df
    .groupby("Ship Mode")
    .agg(
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Delay_Frequency_Percent=("Shipping Lead Time", 
                                 lambda x: (x > shipping_df["Shipping Lead Time"].mean()).mean() * 100),
        Total_Shipments=("Order ID", "count")
    )
    .reset_index()
)

fig_ship_mode = px.bar(
    ship_mode_summary,
    x="Ship Mode",
    y="Average_Lead_Time",
    title="Average Lead Time by Ship Mode",
    labels={
        "Ship Mode": "Ship Mode",
        "Average_Lead_Time": "Average Lead Time (Days)"
    },
    text_auto=".1f"
)

st.plotly_chart(
    fig_ship_mode,
    width="stretch"
)

# Delay frequency comparison
fig_delay = px.bar(
    ship_mode_summary,
    x="Ship Mode",
    y="Delay_Frequency_Percent",
    title="Delay Frequency by Ship Mode",
    labels={
        "Ship Mode": "Ship Mode",
        "Delay_Frequency_Percent": "Delay Frequency (%)"
    },
    text_auto=".1f"
)

st.plotly_chart(
    fig_delay,
    width="stretch"
)

# ---------------------------------------------------------
# Route Drill-Down
# ---------------------------------------------------------

st.markdown("---")
st.header("🔎 Route Drill-Down")

# Start with the cleaned dataset
drill_df = df.copy()

# Calculate delay status for Route Drill-Down
overall_avg_lead = df["Shipping Lead Time"].mean()

drill_df["Delayed"] = (
    drill_df["Shipping Lead Time"] > overall_avg_lead
)

# Apply Factory filter
if selected_factory != "All":
    drill_df = drill_df[
        drill_df["Factory"] == selected_factory
    ]

# Apply State/Province filter
if selected_state != "All":
    drill_df = drill_df[
        drill_df["State/Province"] == selected_state
    ]

# Apply Ship Mode filter
if selected_ship_mode != "All":
    drill_df = drill_df[
        drill_df["Ship Mode"] == selected_ship_mode
    ]

# Apply Date filter
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates

    drill_df = drill_df[
        (drill_df["Order Date"].dt.date >= start_date)
        & (drill_df["Order Date"].dt.date <= end_date)
    ]

if len(drill_df) > 0:

    # Create route name
    drill_df["Route"] = (
        drill_df["Factory"]
        + " → "
        + drill_df["State/Province"]
    )

    # Available routes
    route_options = ["All Routes"] + sorted(
        drill_df["Route"].dropna().unique().tolist()
    )

    selected_route = st.selectbox(
        "Select Route",
        route_options,
        key="route_drilldown"
    )

    # Apply selected route
    if selected_route != "All Routes":
        selected_route_df = drill_df[
            drill_df["Route"] == selected_route
        ].copy()
    else:
        selected_route_df = drill_df.copy()

    # -----------------------------------------------------
    # Route Summary
    # -----------------------------------------------------

    st.subheader("Selected Route Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Shipments",
            f"{len(selected_route_df):,}"
        )

    with col2:
        st.metric(
            "Average Lead Time",
            f"{selected_route_df['Shipping Lead Time'].mean():,.1f} days"
        )

    with col3:
        st.metric(
            "Lead-Time Variability",
            f"{selected_route_df['Shipping Lead Time'].std():,.1f} days"
        )

    with col4:
        delay_rate = (
            selected_route_df["Delayed"].mean() * 100
        )

        st.metric(
            "Delay Frequency",
            f"{delay_rate:.1f}%"
        )

    # -----------------------------------------------------
    # Selected Route Details
    # -----------------------------------------------------

    st.subheader("Selected Route Details")

    route_details = (
        selected_route_df
        .groupby(["Factory", "State/Province"])
        .agg(
            Total_Shipments=("Order ID", "count"),
            Average_Lead_Time=("Shipping Lead Time", "mean"),
            Lead_Time_Variability=("Shipping Lead Time", "std"),
            Delay_Frequency_Percent=("Delayed", "mean")
        )
        .reset_index()
    )

    route_details["Delay_Frequency_Percent"] *= 100

    route_details["Route_Efficiency_Score"] = (
        (100 / route_details["Average_Lead_Time"]) * 1000
    )

    route_details["Average_Lead_Time"] = (
        route_details["Average_Lead_Time"].round(2)
    )

    route_details["Lead_Time_Variability"] = (
        route_details["Lead_Time_Variability"].round(2)
    )

    route_details["Delay_Frequency_Percent"] = (
        route_details["Delay_Frequency_Percent"].round(2)
    )

    route_details["Route_Efficiency_Score"] = (
        route_details["Route_Efficiency_Score"].round(2)
    )

    st.dataframe(
        route_details,
        width="stretch"
    )

    # -----------------------------------------------------
    # Shipment Records
    # -----------------------------------------------------

    st.subheader("Shipment Records for Selected Route")

    shipment_columns = [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Customer ID",
        "City",
        "State/Province",
        "Product Name",
        "Shipping Lead Time"
    ]

    available_columns = [
        col for col in shipment_columns
        if col in selected_route_df.columns
    ]

    st.dataframe(
        selected_route_df[available_columns].sort_values(
            "Shipping Lead Time",
            ascending=False
        ),
        width="stretch"
    )

else:

    st.warning(
        "No shipment records match the selected filters."
    )