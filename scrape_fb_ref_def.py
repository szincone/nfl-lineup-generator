#!/usr/bin/env python3
# scrape_fb_ref_def.py - scrapes pro-football reference and turns into a pd df

import requests, bs4
import pandas as pd

# pandas option so that the df displays all columns
pd.set_option('display.max_columns', None)

# url we're scraping
url_data = "https://www.pro-football-reference.com/years/2017/opp.htm"

res = requests.get(url_data)
res.raise_for_status() # raises exception if an issue with getting the url_data

# making soup
soup = bs4.BeautifulSoup(res.text, "html.parser")

# getting column headers for our data
column_headers = [th.getText() for th in
                  soup.findAll('tr', limit=2)[1].findAll('th')]

# getting data_rows (neccesary for getting player data)
data_rows = soup.findAll('tr')[2:34]

# delete the 'rank row' to get rid of the assertion error
column_headers.remove(column_headers[0])

# renaming column headers because there are duplicates between passing and rushing labels
column_headers[9:13] = ['Pass_Cmp', 'Pass_Att', 'Pass_Yds', 'Pass_TD']
column_headers[16:19] = ['Rush_Att', 'Rush_Yds', 'Rush_TD']

# getting player data(since it's coming from a matrix, you need to make a 2d list)
player_data = [[td.getText() for td in data_rows[i].findAll('td')]
            for i in range(len(data_rows))]

# building our data frame
df_raw = pd.DataFrame(player_data, columns=column_headers)

# there are some blank columns with 'none' in them, so we'll get rid of them with notnull
df_raw = df_raw[df_raw.Tm.notnull()]

# adding a column label for our 'Name' column
df_raw.columns.values[0] = 'Name'

# renaming column header for easier searching
df_raw = df_raw.rename(columns={'Y/P':'YdsPerPlay', 'NY/A':'Pass_YdsPerAtt', 
								'Y/A':'Rush_YdsPerAtt', 'Sc%':'Sc', 'TO%':'TO'})

# replacing apostrophes found in player names
df_raw['Name'] = df_raw['Name'].str.replace("\'", "")

# converting object to nums
df_raw = df_raw.apply(pd.to_numeric, errors='ignore')

# filling in NaN values in the table with '0'
df_raw = df_raw.fillna(0)

# renaming the dataframe
defense = df_raw
