#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import numpy as np
from datetime import datetime

# Request tickers/contracts list from API
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = '/futures/usdt/tickers'
query_param = ''
r = requests.get(host + prefix + url, headers=headers)
ticks = pd.DataFrame(r.json())

# Drop the duplicated contracts and convert to a list in order to request the future rate data
contract = ticks['contract'].drop_duplicates().to_list()

# Create an empty list to append dataframes in the loop below
df_list = []

# Request the future rate for each ticker from API
for t in contract[0:5]:  # !!! sample !!!
    url2 = '/futures/usdt/funding_rate'
    query_param = f'contract={t}'
    r2 = requests.get(host + prefix + url2 + "?" + query_param, headers=headers)
    data = r2.json()

    # Get the rate update frequency (either 4 hours or 8 hours)
    freq = data[0]['t'] - data[1]['t']
    # Calculate the data size we need for the latest 3 days
    times = int(72 / (freq / (60 * 60)))

    filtered_data = data[0:times]

    # Add the contract name
    for item in filtered_data:
        item['contract'] = t

    # Convert data to a dataframe and append it to the list
    df = pd.DataFrame(filtered_data)
    df_list.append(df)

# Concatenate the dataframes from the list
combined_df = pd.concat(df_list, ignore_index=True)

# Print the combined dataframe
print(combined_df)

# Display first 5 rows of the combined dataframe
combined_df.head(5)

# Display dataframe information
combined_df.info()

# Convert the timestamp to a datetime object in format 'YYYY-MM-DD HH:mm'
combined_df['t'] = pd.to_datetime(combined_df['t'], unit='s').dt.strftime('%Y-%m-%d %H:%M')

# Convert funding rate to numeric and multiply by 100
combined_df['r'] = pd.to_numeric(combined_df['r']) * 100

# Rename columns
combined_df = combined_df.rename(columns={'r': 'funding_rate', 't': 'datetime'})

# Display first 5 rows of the updated dataframe
combined_df.head(5)

# Function to get the first third of the data
def get_first_third(group):
    n = len(group) // 3
    return group.head(n)

# Function to get the first two thirds of the data
def get_two_third(group):
    n = 2 * len(group) // 3
    return group.head(n)

# Apply the function to get the first third of the data
df_first_third = combined_df.groupby('contract', group_keys=False).apply(get_first_third)

# Apply the function to get the first two thirds of the data
df_two_third = combined_df.groupby('contract', group_keys=False).apply(get_two_third)

# Calculate the average funding rate for the first third of data
df_first_third_avg = (df_first_third.groupby('contract')['funding_rate']
                      .mean().reset_index()
                      .rename(columns={'funding_rate': 'funding_rate_1day'})
                      .sort_values(by='funding_rate_1day', ascending=False))

# Calculate the average funding rate for the first two thirds of data
df_two_third_avg = (df_two_third.groupby('contract')['funding_rate']
                    .mean().reset_index()
                    .rename(columns={'funding_rate': 'funding_rate_2days'})
                    .sort_values(by='funding_rate_2days', ascending=False))

# Calculate the average funding rate for all three days
df_all_avg = (combined_df.groupby('contract')['funding_rate']
              .mean().reset_index()
              .rename(columns={'funding_rate': 'funding_rate_3days'})
              .sort_values(by='funding_rate_3days', ascending=False))

# Merge the average funding rates into one dataframe
df2 = df_first_third_avg.merge(df_two_third_avg, on='contract')
final_df = df2.merge(df_all_avg, on='contract')

# Display the final dataframe
print(final_df)


df_first_third_avg.to_csv('rate_1day.txt',sep='\t', index=False)
df_two_third_avg.to_csv('rate_2days.txt',sep='\t', index=False)
df_all_avg.to_csv('rate_3days.txt',sep='\t', index=False)