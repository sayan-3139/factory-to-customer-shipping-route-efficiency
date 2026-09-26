import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("Nassau_Candy_Cleaned.csv")

# Display basic information
print("Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nBasic Statistics:")
print(df.describe())

print("\nSales Statistics:")
print(df["Sales"].describe())

print("\nTotal Sales:")
print(df["Sales"].sum())

print("\nTotal Units Sold:")
print(df["Units"].sum())

print("\nTotal Gross Profit:")
print(df["Gross Profit"].sum())

print("\nSales by Division:")
print(df.groupby("Division")["Sales"].sum())

print("\nSales by Region:")
print(df.groupby("Region")["Sales"].sum())

print("\nSales by Ship Mode:")
print(df.groupby("Ship Mode")["Sales"].sum())

print("\nTop 10 Products by Sales:")
print(
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# 1. Sales by Division
df.groupby("Division")["Sales"].sum().plot(kind="bar")
plt.title("Sales by Division")
plt.xlabel("Division")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# 2. Sales by Region
df.groupby("Region")["Sales"].sum().plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# 3. Sales by Ship Mode
df.groupby("Ship Mode")["Sales"].sum().plot(kind="bar")

plt.title("Sales by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# 6. Gross Profit by Division

profit_by_division = df.groupby("Division")["Gross Profit"].sum()

print("\nGross Profit by Division:")
print(profit_by_division)

profit_by_division.plot(kind="bar")

plt.title("Gross Profit by Division")
plt.xlabel("Division")
plt.ylabel("Gross Profit")

plt.tight_layout()
plt.show()

# 7. Gross Profit by Region

profit_by_region = df.groupby("Region")["Gross Profit"].sum()

print("\nGross Profit by Region:")
print(profit_by_region)

profit_by_region.plot(kind="bar")

plt.title("Gross Profit by Region")
plt.xlabel("Region")
plt.ylabel("Gross Profit")

plt.tight_layout()
plt.show()

# 8. Gross Profit by Ship Mode

profit_by_ship_mode = df.groupby("Ship Mode")["Gross Profit"].sum()

print("\nGross Profit by Ship Mode:")
print(profit_by_ship_mode)

profit_by_ship_mode.plot(kind="bar")

plt.title("Gross Profit by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Gross Profit")

plt.tight_layout()
plt.show()

# 9. Top 10 Products by Sales

top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Products by Sales:")
print(top_products)

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product Name")

plt.tight_layout()
plt.show()

# 10. Shipping Lead Time Analysis

print("\nShipping Lead Time Statistics:")
print(df["Shipping Lead Time"].describe())

print("\nAverage Shipping Lead Time:")
print(df["Shipping Lead Time"].mean())

# Shipping Lead Time by Ship Mode
lead_time_by_mode = df.groupby("Ship Mode")["Shipping Lead Time"].mean()

print("\nAverage Shipping Lead Time by Ship Mode:")
print(lead_time_by_mode)

lead_time_by_mode.plot(kind="bar")

plt.title("Average Shipping Lead Time by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Average Lead Time (Days)")

plt.tight_layout()
plt.show()

# 11. Average Shipping Lead Time by Region

lead_time_by_region = df.groupby("Region")["Shipping Lead Time"].mean()

print("\nAverage Shipping Lead Time by Region:")
print(lead_time_by_region)

lead_time_by_region.plot(kind="bar")

plt.title("Average Shipping Lead Time by Region")
plt.xlabel("Region")
plt.ylabel("Average Lead Time (Days)")

plt.tight_layout()
plt.show()

# 12. Factory to Customer Region Route Analysis

route_analysis = (
    df.groupby(["Division", "Region"])
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

print("\nFactory to Customer Region Route Analysis:")
print(route_analysis)

# 13. Rank Routes by Average Shipping Lead Time

route_ranking = route_analysis.sort_values(
    by="Average_Lead_Time",
    ascending=True
)

print("\nRoutes Ranked from Fastest to Slowest:")
print(route_ranking)

# 14. Check geographic/factory-related fields

print("\nUnique Country/Region values:")
print(df["Country/Region"].unique())

print("\nUnique Regions:")
print(df["Region"].unique())

print("\nUnique States:")
print(df["State/Province"].nunique())

print("\nUnique Cities:")
print(df["City"].nunique())

print("\nUnique Division values:")
print(df["Division"].unique())

print("\nUnique Country/Region values:")
print(df["Country/Region"].unique())

print("\nSample State/Province values:")
print(df["State/Province"].unique()[:30])

print("\nSample City values:")
print(df["City"].unique()[:30])

# 15. Map products to factories

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

print("\nFactory Distribution:")
print(df["Factory"].value_counts())

print("\nProducts with Missing Factory:")
print(df[df["Factory"].isnull()]["Product Name"].unique())

# 16. Factory to Customer Region Route Analysis

factory_region_analysis = (
    df.groupby(["Factory", "Region"])
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std")
    )
    .reset_index()
)

print("\nFactory to Customer Region Route Analysis:")
print(factory_region_analysis.to_string(index=False))

# 17. Rank Factory to Customer Region routes
# Fastest route = lowest average lead time

route_ranking = factory_region_analysis.sort_values(
    by="Average_Lead_Time",
    ascending=True
).reset_index(drop=True)

print("\nFactory to Customer Region Routes - Fastest to Slowest:")
print(route_ranking.to_string(index=False))

# 18. Top 10 most efficient routes

top_10_routes = route_ranking.head(10)

print("\nTop 10 Most Efficient Factory to Customer Region Routes:")
print(top_10_routes.to_string(index=False))


# 19. Bottom 10 least efficient routes

bottom_10_routes = route_ranking.tail(10).sort_values(
    by="Average_Lead_Time",
    ascending=False
)

print("\nBottom 10 Least Efficient Factory to Customer Region Routes:")
print(bottom_10_routes.to_string(index=False))

# 20. Factory to Customer State Route Analysis

factory_state_analysis = (
    df.groupby(["Factory", "State/Province"])
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std")
    )
    .reset_index()
)

print("\nFactory to Customer State Route Analysis:")
print(factory_state_analysis.to_string(index=False))

# 21. Rank Factory to Customer State routes

state_route_ranking = factory_state_analysis.sort_values(
    by="Average_Lead_Time",
    ascending=False
).reset_index(drop=True)

print("\nFactory to Customer State Routes - Slowest to Fastest:")
print(state_route_ranking.to_string(index=False))

# 22. Identify high-volume Factory to Customer State routes

high_volume_state_routes = factory_state_analysis[
    factory_state_analysis["Total_Shipments"] >= 50
].sort_values(
    by="Average_Lead_Time",
    ascending=False
)

print("\nHigh-Volume Factory to Customer State Routes:")
print(high_volume_state_routes.to_string(index=False))

# 23. Calculate Route Efficiency Score

route_efficiency = factory_state_analysis.copy()

# Higher score = better efficiency
route_efficiency["Route_Efficiency_Score"] = (
    100 / route_efficiency["Average_Lead_Time"]
) * 1000

route_efficiency = route_efficiency.sort_values(
    by="Route_Efficiency_Score",
    ascending=False
)

print("\nRoute Efficiency Score:")
print(route_efficiency.to_string(index=False))

# 24. Ship Mode Comparison

ship_mode_analysis = (
    df.groupby("Ship Mode")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

print("\nShip Mode Comparison:")
print(ship_mode_analysis.to_string(index=False))

# 25. Delay Frequency Analysis

overall_average_lead_time = df["Shipping Lead Time"].mean()

df["Delayed"] = (
    df["Shipping Lead Time"] > overall_average_lead_time
)

delay_frequency = (
    df.groupby("Ship Mode")["Delayed"]
    .mean()
    .mul(100)
    .reset_index(name="Delay_Frequency_Percent")
)

print("\nOverall Average Lead Time:")
print(overall_average_lead_time)

print("\nDelay Frequency by Ship Mode:")
print(delay_frequency.to_string(index=False))

# 26. Final Route KPI Table

final_route_kpi = factory_state_analysis.copy()

# Route Efficiency Score
final_route_kpi["Route_Efficiency_Score"] = (
    100 / final_route_kpi["Average_Lead_Time"]
) * 1000

# Delay Frequency for each route
overall_average_lead_time = df["Shipping Lead Time"].mean()

route_delay = (
    df.groupby(["Factory", "State/Province"])["Shipping Lead Time"]
    .apply(lambda x: (x > overall_average_lead_time).mean() * 100)
    .reset_index(name="Delay_Frequency_Percent")
)

# Merge delay frequency into route KPI table
final_route_kpi = final_route_kpi.merge(
    route_delay,
    on=["Factory", "State/Province"],
    how="left"
)

# Arrange columns
final_route_kpi = final_route_kpi[
    [
        "Factory",
        "State/Province",
        "Total_Shipments",
        "Average_Lead_Time",
        "Lead_Time_Variability",
        "Delay_Frequency_Percent",
        "Route_Efficiency_Score"
    ]
]

print("\nFinal Route KPI Table:")
print(final_route_kpi.to_string(index=False))

# 27. Geographic Bottlenecks

geographic_bottlenecks = (
    final_route_kpi[
        final_route_kpi["Total_Shipments"] >= 50
    ]
    .sort_values(
        by="Average_Lead_Time",
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Geographic Bottlenecks:")
print(geographic_bottlenecks.to_string(index=False))

# 28. High-Volume Routes with Poor Performance
high_volume_poor_routes = final_route_kpi[
    (final_route_kpi["Total_Shipments"] >= 100) &
    (final_route_kpi["Average_Lead_Time"] > overall_average_lead_time)
].sort_values(
    by="Average_Lead_Time",
    ascending=False
)

print("\nHigh-Volume Routes with Poor Performance:")
print(high_volume_poor_routes.to_string(index=False))

# 30. Detect Congestion-Prone States

state_congestion = (
    df.groupby("State/Province")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std"),
        Delay_Frequency_Percent=("Delayed", "mean")
    )
    .reset_index()
)

state_congestion["Delay_Frequency_Percent"] = (
    state_congestion["Delay_Frequency_Percent"] * 100
)

# Focus on states with meaningful shipment volume
congestion_prone_states = state_congestion[
    state_congestion["Total_Shipments"] >= 50
].sort_values(
    by=["Average_Lead_Time", "Total_Shipments"],
    ascending=[False, False]
)

print("\nCongestion-Prone States:")
print(congestion_prone_states.to_string(index=False))

# 31. Detect Congestion-Prone Regions

region_congestion = (
    df.groupby("Region")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std"),
        Delay_Frequency_Percent=("Delayed", "mean")
    )
    .reset_index()
)

region_congestion["Delay_Frequency_Percent"] = (
    region_congestion["Delay_Frequency_Percent"] * 100
)

region_congestion = region_congestion.sort_values(
    by="Average_Lead_Time",
    ascending=False
)

print("\nCongestion-Prone Regions:")
print(region_congestion.to_string(index=False))

# 32. Ship Mode Performance Analysis

ship_mode_performance = (
    df.groupby("Ship Mode")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std"),
        Delay_Frequency_Percent=("Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

ship_mode_performance["Delay_Frequency_Percent"] = (
    ship_mode_performance["Delay_Frequency_Percent"] * 100
)

print("\nShip Mode Performance Analysis:")
print(ship_mode_performance.to_string(index=False))

# 33. Standard vs Expedited Shipping Comparison

df["Shipping_Category"] = df["Ship Mode"].apply(
    lambda x: "Standard Shipping"
    if x == "Standard Class"
    else "Expedited Shipping"
)

shipping_category_analysis = (
    df.groupby("Shipping_Category")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std"),
        Delay_Frequency_Percent=("Delayed", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

shipping_category_analysis["Delay_Frequency_Percent"] = (
    shipping_category_analysis["Delay_Frequency_Percent"] * 100
)

print("\nStandard vs Expedited Shipping:")
print(shipping_category_analysis.to_string(index=False))

# 34. Descriptive Cost-Time Trade-off

shipping_category_analysis["Profit_per_Shipment"] = (
    shipping_category_analysis["Total_Profit"] /
    shipping_category_analysis["Total_Shipments"]
)

shipping_category_analysis["Sales_per_Shipment"] = (
    shipping_category_analysis["Total_Sales"] /
    shipping_category_analysis["Total_Shipments"]
)

print("\nDescriptive Cost-Time Trade-off:")
print(
    shipping_category_analysis[
        [
            "Shipping_Category",
            "Average_Lead_Time",
            "Delay_Frequency_Percent",
            "Sales_per_Shipment",
            "Profit_per_Shipment"
        ]
    ].to_string(index=False)
)



# 35. Final KPI Dataset for Dashboard

dashboard_kpi = final_route_kpi.copy()

# Round values for a cleaner dashboard dataset
dashboard_kpi["Average_Lead_Time"] = dashboard_kpi[
    "Average_Lead_Time"
].round(2)

dashboard_kpi["Lead_Time_Variability"] = dashboard_kpi[
    "Lead_Time_Variability"
].round(2)

dashboard_kpi["Delay_Frequency_Percent"] = dashboard_kpi[
    "Delay_Frequency_Percent"
].round(2)

dashboard_kpi["Route_Efficiency_Score"] = dashboard_kpi[
    "Route_Efficiency_Score"
].round(2)

# Save KPI dataset
dashboard_kpi.to_csv(
    "Route_Efficiency_KPI.csv",
    index=False
)

print("\nFinal Dashboard KPI Dataset:")
print(dashboard_kpi.to_string(index=False))

print("\nKPI dataset saved as Route_Efficiency_KPI.csv")
