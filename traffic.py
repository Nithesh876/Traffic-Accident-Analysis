# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'traffic_accidents1.csv'  # Path to your CSV file
traffic_data = pd.read_csv(file_path)

# Data overview
print("Data Information:")
print(traffic_data.info())
print("\nFirst 5 Rows of the Dataset:")
print(traffic_data.head())

# Handle missing values if any
# Fill missing numeric values with 0
numeric_columns = traffic_data.select_dtypes(include='number').columns
traffic_data[numeric_columns] = traffic_data[numeric_columns].fillna(0)

# Fill missing district names with "Unknown"
traffic_data['District'] = traffic_data['District'].fillna('Unknown')

# Summarize total crashes and deaths by year
yearly_data = {
    'Year': ['2020', '2021', '2022', '2023'],
    'Total Crashes': [
        traffic_data['Road Crashes 2020'].sum(),
        traffic_data['Road Crashes 2021'].sum(),
        traffic_data['Road Crashes 2022'].sum(),
        traffic_data['Road Crashes 2023'].sum()
    ],
    'Total Deaths': [
        traffic_data['Deaths 2020'].sum(),
        traffic_data['Deaths 2021'].sum(),
        traffic_data['Deaths 2022'].sum(),
        traffic_data['Deaths 2023'].sum()
    ]
}

# Convert yearly data to DataFrame for easier plotting
yearly_df = pd.DataFrame(yearly_data)

# Plotting yearly trends for crashes and deaths
plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly_df, x='Year', y='Total Crashes', marker='o', label='Total Crashes')
sns.lineplot(data=yearly_df, x='Year', y='Total Deaths', marker='o', label='Total Deaths')
plt.title("Yearly Trend of Road Crashes and Deaths (2020-2023)")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend()
plt.show()

# District-wise analysis of total crashes and deaths from 2020 to 2023
# Using .copy() to avoid SettingWithCopyWarning
district_summary = traffic_data[['District', 'Road Crashes 2020', 'Deaths 2020', 
                                 'Road Crashes 2021', 'Deaths 2021', 
                                 'Road Crashes 2022', 'Deaths 2022', 
                                 'Road Crashes 2023', 'Deaths 2023']].copy()

# Calculate total crashes and deaths over all years for each district
district_summary['Total Crashes (2020-2023)'] = district_summary[
    ['Road Crashes 2020', 'Road Crashes 2021', 'Road Crashes 2022', 'Road Crashes 2023']
].sum(axis=1)
district_summary['Total Deaths (2020-2023)'] = district_summary[
    ['Deaths 2020', 'Deaths 2021', 'Deaths 2022', 'Deaths 2023']
].sum(axis=1)

# Display top 5 districts with the highest crashes and deaths
top_crashes_districts = district_summary.nlargest(5, 'Total Crashes (2020-2023)')[['District', 'Total Crashes (2020-2023)']]
top_deaths_districts = district_summary.nlargest(5, 'Total Deaths (2020-2023)')[['District', 'Total Deaths (2020-2023)']]

print("\nTop 5 Districts by Total Crashes (2020-2023):")
print(top_crashes_districts)
print("\nTop 5 Districts by Total Deaths (2020-2023):")
print(top_deaths_districts)

# Correlation analysis between crashes and deaths for each year
correlations = {
    '2020': traffic_data['Road Crashes 2020'].corr(traffic_data['Deaths 2020']),
    '2021': traffic_data['Road Crashes 2021'].corr(traffic_data['Deaths 2021']),
    '2022': traffic_data['Road Crashes 2022'].corr(traffic_data['Deaths 2022']),
    '2023': traffic_data['Road Crashes 2023'].corr(traffic_data['Deaths 2023'])
}
print("\nYearly Correlations between Road Crashes and Deaths:", correlations)

# Visualizing top districts by crashes and deaths
plt.figure(figsize=(12, 6))

# Top 5 Districts by Total Crashes
plt.subplot(1, 2, 1)
sns.barplot(data=top_crashes_districts, x='Total Crashes (2020-2023)', y='District', hue='District', palette='Blues_d', dodge=False, legend=False)
plt.title('Top 5 Districts by Total Crashes (2020-2023)')

# Top 5 Districts by Total Deaths
plt.subplot(1, 2, 2)
sns.barplot(data=top_deaths_districts, x='Total Deaths (2020-2023)', y='District', hue='District', palette='Reds_d', dodge=False, legend=False)
plt.title('Top 5 Districts by Total Deaths (2020-2023)')

plt.tight_layout()
plt.show()

# Scatter Plot: Relationship between Crashes and Deaths for each year
plt.figure(figsize=(12, 8))

for i, year in enumerate(['2020', '2021', '2022', '2023']):
    plt.subplot(2, 2, i+1)
    sns.scatterplot(x=traffic_data[f'Road Crashes {year}'], y=traffic_data[f'Deaths {year}'])
    plt.title(f"Crashes vs. Deaths ({year})")
    plt.xlabel("Road Crashes")
    plt.ylabel("Deaths")

plt.tight_layout()
plt.show()

# Scatter Plot: Relationship between Total Crashes and Total Deaths per District
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Total Crashes (2020-2023)', y='Total Deaths (2020-2023)', data=district_summary)
plt.title("Total Crashes vs. Total Deaths per District (2020-2023)")
plt.xlabel("Total Crashes (2020-2023)")
plt.ylabel("Total Deaths (2020-2023)")
plt.show()

# Pie charts for the distribution of crashes and deaths in top 5 districts
plt.figure(figsize=(12, 6))

# Pie chart for Top 5 Districts by Total Crashes
plt.subplot(1, 2, 1)
plt.pie(top_crashes_districts['Total Crashes (2020-2023)'], labels=top_crashes_districts['District'], autopct='%1.1f%%', colors=sns.color_palette('Blues_d', n_colors=5))
plt.title('Proportion of Total Crashes (2020-2023) in Top 5 Districts')

# Pie chart for Top 5 Districts by Total Deaths
plt.subplot(1, 2, 2)
plt.pie(top_deaths_districts['Total Deaths (2020-2023)'], labels=top_deaths_districts['District'], autopct='%1.1f%%', colors=sns.color_palette('Reds_d', n_colors=5))
plt.title('Proportion of Total Deaths (2020-2023) in Top 5 Districts')

plt.tight_layout()
plt.show()
