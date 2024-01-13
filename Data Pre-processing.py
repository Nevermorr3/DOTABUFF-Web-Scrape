# Import libraries
import pandas as pd
import re
from datetime import datetime

# Specify file path
file_path = 'DOTA Esports Data.xlsx'

# Read Excel file into a DataFrame
esports_df = pd.read_excel(file_path)

# Cleaning the 'Won' column

# Check the format of a single item in the 'Won' column
print(esports_df['Won'][0])

# Strip the '[]'
esports_df['Won'] = esports_df['Won'].apply(lambda x: x.strip("[]"))

print(esports_df['Won'][0])

# Convert items within '' to list item
esports_df['Won'] = esports_df['Won'].apply(lambda x: re.findall(r"'(.*?)'", x))

# Check if the modifications are executed correctly
print(esports_df['Won'][0])


# Function to remove "/assets/heroes/"
def remove_prefix(text):
    return text.replace('/assets/heroes/', '')


# Function to keep only the part before the last hyphen
def keep_before_last_hyphen(text):
    return text[:text.rfind("-")] if "-" in text else text


# Function to replace '-' with ' '
def replace_with_space(text):
    return text.replace('-', ' ')


# Apply the functions to the 'Won' column in the esports_df DataFrame
esports_df['Won'] = esports_df['Won'].apply(lambda x: [remove_prefix(item) for item in x])
esports_df['Won'] = esports_df['Won'].apply(lambda x: [keep_before_last_hyphen(item) for item in x])
esports_df['Won'] = esports_df['Won'].apply(lambda x: [replace_with_space(item) for item in x])

# Check if the modifications are executed correctly
print(esports_df['Won'])

# Cleaning the 'Lost' column

# Check the format of a single item in the 'Lost' column
print(esports_df['Lost'][0])

# Strip the '[]'
esports_df['Lost'] = esports_df['Lost'].apply(lambda x: x.strip("[]"))

# Check if the modifications are executed correctly
print(esports_df['Lost'][0])

# Convert items within '' to list item
esports_df['Lost'] = esports_df['Lost'].apply(lambda x: re.findall(r"'(.*?)'", x))

# Check if the modifications are executed correctly
print(esports_df['Lost'][0])

# Apply the functions to the 'Lost' column in the esports_df DataFrame
esports_df['Lost'] = esports_df['Lost'].apply(lambda x: [remove_prefix(item) for item in x])
esports_df['Lost'] = esports_df['Lost'].apply(lambda x: [keep_before_last_hyphen(item) for item in x])
esports_df['Lost'] = esports_df['Lost'].apply(lambda x: [replace_with_space(item) for item in x])

# Check if the modifications are executed correctly
print(esports_df['Lost'])

# Cleaning the 'Date_Time' column

# Convert 'Date_Time' column to datetime object
esports_df['Date_Time'] = pd.to_datetime(esports_df['Date_Time'], format='%a, %d %b %Y %H:%M:%S %z')

# Extract date and time into separate columns
esports_df['Date'] = esports_df['Date_Time'].dt.date
esports_df['Time'] = esports_df['Date_Time'].dt.time

# Check if the modifications are executed correctly
print(esports_df[['Date', 'Time']])

# Cleaning the Duration column

# Add "00:" to strings with only one ":" character
esports_df['Duration'] = esports_df['Duration'].apply(lambda x: f"00:{x}" if x.count(':') == 1 else x)

# Add "0" to strings with only one character before ":"
esports_df['Duration'] = esports_df['Duration'].apply(lambda x: '0' + x if len(x.split(':')[0]) == 1 else x)

# Extract the first eight characters
esports_df['Duration'] = esports_df['Duration'].str[:8]

# Convert the 'Durations' column to time format
esports_df['Duration'] = esports_df['Duration'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

# Check if the modifications are executed correctly
print(esports_df['Duration'])

# Cleaning the Series column

# Remove the 'Series ' prefix
esports_df['Series'] = esports_df['Series'].str.replace('Series ', '')

# Convert the column to strings
esports_df['Series'] = esports_df['Series'].astype(str)

# Check if the modifications are executed correctly
print(esports_df['Series'])

# Create the cleaned DataFrame
cleaned_esports_df = esports_df[['Match_ID', 'Series', 'Region', 'Date', 'Time', 'Won', 'Lost', 'Duration']]

# Display all columns and their contents
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Check if the DataFrame has been created correctly
print(cleaned_esports_df)

# Write to Excel file
cleaned_esports_df.to_excel("Cleaned DOTABUFF Esports Data.xlsx", index=False)
