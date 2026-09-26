import pandas as pd

# 1. Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# 2. Basic information
print("Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

# 3. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 4. Check duplicate rows
print("\nDuplicate Rows:", df.duplicated().sum())

# 5. Convert dates
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# 6. Check invalid dates
print("\nInvalid Order Dates:", df["Order Date"].isna().sum())
print("Invalid Ship Dates:", df["Ship Date"].isna().sum())

# 7. Calculate shipping lead time
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# 8. Check negative lead times
print(
    "\nNegative Lead Times:",
    (df["Shipping Lead Time"] < 0).sum()
)

# 9. Check zero lead times
print(
    "Zero Lead Times:",
    (df["Shipping Lead Time"] == 0).sum()
)

# 10. Lead-time statistics
print("\nShipping Lead Time Statistics:")
print(df["Shipping Lead Time"].describe())

# 11. Check ship modes
print("\nShip Modes:")
print(df["Ship Mode"].value_counts())

# 12. Check regions
print("\nRegions:")
print(df["Region"].value_counts())

# 13. Check divisions
print("\nProduct Divisions:")
print(df["Division"].value_counts())

# 14. Save cleaned dataset
df.to_csv("Nassau_Candy_Cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")