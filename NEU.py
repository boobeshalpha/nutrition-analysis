import pandas as pd
import requests
import pycountry
import os

# WHO API URLs
urls = {
    "obesity_adult": "https://ghoapi.azureedge.net/api/NCD_BMI_30C",
    "obesity_child": "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C",
    "malnutrition_adult": "https://ghoapi.azureedge.net/api/NCD_BMI_18C",
    "malnutrition_child": "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"
}

# Function to fetch data from API
def fetch_who_data(url):
    response = requests.get(url)
    data = response.json()['value']
    return pd.DataFrame(data)

# Load all datasets
df_obesity_adult = fetch_who_data(urls['obesity_adult'])
df_obesity_child = fetch_who_data(urls['obesity_child'])
df_malnutrition_adult = fetch_who_data(urls['malnutrition_adult'])
df_malnutrition_child = fetch_who_data(urls['malnutrition_child'])
# Keep required columns and add age_group
def clean_and_tag(df, age_group):
    df = df[['ParentLocation', 'Dim1', 'TimeDim', 'Low', 'High', 'NumericValue', 'SpatialDim']].copy()
    df.loc[:, 'age_group'] = age_group
    return df

# Tag with age group
df_obesity_adult = clean_and_tag(df_obesity_adult, 'Adult')
df_obesity_child = clean_and_tag(df_obesity_child, 'Child/Adolescent')
df_malnutrition_adult = clean_and_tag(df_malnutrition_adult, 'Adult')
df_malnutrition_child = clean_and_tag(df_malnutrition_child, 'Child/Adolescent')

# Combine obesity and malnutrition datasets
df_obesity = pd.concat([df_obesity_adult, df_obesity_child], ignore_index=True)
df_malnutrition = pd.concat([df_malnutrition_adult, df_malnutrition_child], ignore_index=True)
def preprocess(df):
    df = df.rename(columns={
        'ParentLocation': 'Region',
        'Dim1': 'Gender',
        'TimeDim': 'Year',
        'Low': 'LowerBound',
        'High': 'UpperBound',
        'NumericValue': 'Mean_Estimate',
        'SpatialDim': 'Country'
    })
    df = df[df['Year'].between(2012, 2022)]
    df['Gender'] = df['Gender'].replace({'BTSX': 'Both', 'MLE': 'Male', 'FMLE': 'Female'})
    return df

df_obesity = preprocess(df_obesity)
df_malnutrition = preprocess(df_malnutrition)


def convert_country(code):
    try:
        return pycountry.countries.get(alpha_3=code).name
    except:
        return code

# Handle special cases
special_cases = {
    'GLOBAL': 'Global',
    'WB_LMI': 'Low & Middle Income',
    'WB_HI': 'High Income',
    'WB_LI': 'Low Income',
    'EMR': 'Eastern Mediterranean Region',
    'EUR': 'Europe',
    'AFR': 'Africa',
    'SEAR': 'South-East Asia Region',
    'WPR': 'Western Pacific Region',
    'AMR': 'Americas Region',
    'WB_UMI': 'Upper Middle Income'
}

def map_country(code):
    return special_cases.get(code, convert_country(code))

df_obesity['Country'] = df_obesity['Country'].apply(map_country)
df_malnutrition['Country'] = df_malnutrition['Country'].apply(map_country)
 # CI Width
df_obesity['CI_Width'] = df_obesity['UpperBound'] - df_obesity['LowerBound']
df_malnutrition['CI_Width'] = df_malnutrition['UpperBound'] - df_malnutrition['LowerBound']

# Obesity Level Categorization
def obesity_category(x):
    if x >= 30: return 'High'
    elif 25 <= x < 30: return 'Moderate'
    else: return 'Low'

# Malnutrition Level Categorization
def malnutrition_category(x):
    if x >= 20: return 'High'
    elif 10 <= x < 20: return 'Moderate'
    else: return 'Low'

df_obesity['obesity_level'] = df_obesity['Mean_Estimate'].apply(obesity_category)
df_malnutrition['malnutrition_level'] = df_malnutrition['Mean_Estimate'].apply(malnutrition_category)
df_obesity.to_csv("cleaned_obesity_data.csv", index=False)
df_malnutrition.to_csv("cleaned_malnutrition_data.csv", index=False)

# Load cleaned CSV files
df_obesity.to_csv("C:/Users/keert/Documents/cleaned_obesity_data.csv", index=False)
df_malnutrition.to_csv("C:/Users/keert/Documents/cleaned_malnutrition_data.csv", index=False)


print("✅ Script completed successfully!")
print("Files saved at:", os.getcwd())
print("cleaned_obesity_data.csv and cleaned_malnutrition_data.csv")
print("You can now use these files for further analysis or visualization.")