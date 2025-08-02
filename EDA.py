# --- Required Imports ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pycountry
import os

# --- Load Cleaned Datasets ---
df_obesity = pd.read_csv('cleaned_obesity_data.csv')
df_malnutrition = pd.read_csv('cleaned_malnutrition_data.csv')

# --- Combine Obesity and Malnutrition Data ---
df = pd.concat([df_obesity, df_malnutrition], ignore_index=True)

# --- 1. Preview the Data ---
print("✅ First 5 rows:")
print(df.head())

print("\n✅ Data Info:")
print(df.info())

print("\n✅ Descriptive Statistics:")
print(df.describe())

# --- 2. Check for Missing Values ---
print("\n✅ Missing Values:")
print(df.isnull().sum())

# --- 3. Unique Values Per Column ---
print("\n✅ Unique Values Per Column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()}")

# --- 4. Distribution Plot: Mean_Estimate ---
if 'Mean_Estimate' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Mean_Estimate'], kde=True, color='skyblue')
    plt.title('Distribution of Mean Estimate')
    plt.xlabel('Mean_Estimate')
    plt.ylabel('Frequency')
    # plt.savefig("mean_estimate_distribution.png")
    plt.show(block=True)

# --- 5. Distribution Plot: CI_Width ---
if 'CI_Width' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df['CI_Width'], kde=True, color='salmon')
    plt.title('Distribution of Confidence Interval Width')
    plt.xlabel('CI_Width')
    plt.ylabel('Frequency')
    # plt.savefig("ci_width_distribution.png")
    plt.show(block=True)

# --- 6. Line Plot: Average Estimate Over Time ---
if 'Year' in df.columns:
    yearly_trend = df.groupby('Year')['Mean_Estimate'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=yearly_trend, x='Year', y='Mean_Estimate', marker='o')
    plt.title('Average Mean Estimate Over Time')
    plt.xlabel('Year')
    plt.ylabel('Mean Estimate')
    plt.grid(True)
    # plt.savefig("yearly_trend.png")
    plt.show(block=True)

# --- 7. Box Plot: Region vs Mean Estimate ---
if 'Region' in df.columns:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Region', y='Mean_Estimate')
    plt.xticks(rotation=45)
    plt.title('Mean Estimate by Region')
    plt.tight_layout()
    # plt.savefig("boxplot_region_mean_estimate.png")
    plt.show(block=True)

# --- 8. Scatter Plot: CI Width vs Mean Estimate ---
if 'CI_Width' in df.columns and 'Mean_Estimate' in df.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='CI_Width', y='Mean_Estimate', hue=df['Region'] if 'Region' in df.columns else None)
    plt.title('CI Width vs Mean Estimate')
    plt.xlabel('CI_Width')
    plt.ylabel('Mean_Estimate')
    plt.legend(loc='best', fontsize='small')
    # plt.savefig("scatter_ci_vs_mean.png")
    plt.show(block=True)

# --- 9. Correlation Heatmap ---
plt.figure(figsize=(8, 6))
numeric_df = df.select_dtypes(include='number')
sns.heatmap(numeric_df.corr(), annot=True, cmap='YlGnBu')
plt.title('Correlation Heatmap')
# plt.savefig("correlation_heatmap.png")
plt.show(block=True)
