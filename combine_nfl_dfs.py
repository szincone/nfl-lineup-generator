#!/usr/bin/env python3
# combine_nfl_dfs.py - combines pro-football_ref dataframes with csv_data from draftkings

import os, sys, random
import pandas as pd

# sets path for importing needed dataframes
path = '' # put the path that contains your python files here
sys.path.insert(0, path)

# imports needed df
from scrape_fb_ref_off import stats
from scrape_fb_ref_def import defense

# import draftking csv
csv_path = '' # put your dk_csv path here
data = pd.read_csv(csv_path)

# csv data as pandas df
dk = pd.DataFrame(data)

# clean up dk_dataframe to better merge with pro-football_ref dataframes
dk['Name'] = dk['Name'].str.replace(" II", "")
dk['Name'] = dk['Name'].str.replace(" V ", "")
dk['Name'] = dk['Name'].str.replace(" Jr.", "")
dk['Name'] = dk['Name'].str.replace("\'", "")
dk['Name'] = dk['Name'].str.replace(".", "")


# getting rid of players from draftking dk
dk_def = dk[dk['Position'] == 'DST']

# getting rid of defense from draft kings df
dk_players = dk[dk['Position'] != 'DST']

#combining draftkings and stats dfs
combo_raw = pd.merge_ordered(stats, dk_players, on='Name')

#getting rid of players who aren't playing
combo_raw = combo_raw[combo_raw.Salary.notnull()]

#renaming merged dataframe
combo = combo_raw
