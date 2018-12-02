#! python
# combine_nfl_dfs.py - combines pro-football_ref scraper data (def and off) with csv_data from draftkings (3 dataframes to 1)
from scrapers.scrape_fb_ref_def import defense
from scrapers.scrape_fb_ref_off import stats
import os
import sys
import random
import pandas as pd
from dotenv import load_dotenv

# loading our environment variables
load_dotenv()


# import draftking csv which doesn't exist,
# you need to add the draftking csv to the csv_files folder
dk_csv_file = os.getenv("csv")
dk_csv_path = f'./csv_files/{dk_csv_file}'
data = pd.read_csv(dk_csv_path)

# csv data as pandas df
dk = pd.DataFrame(data)

# replacing unwanted chars found in player names
dk['Name'] = dk['Name'].str.replace(" II", "")
dk['Name'] = dk['Name'].str.replace(" V ", "")
dk['Name'] = dk['Name'].str.replace(" Jr.", "")
dk['Name'] = dk['Name'].str.replace("\'", "")
dk['Name'] = dk['Name'].str.replace(".", "")


#  getting rid of players from draftking dk
dk_def = dk[dk['Position'] == 'DST']

#  getting rid of defense from draft kings df
dk_players = dk[dk['Position'] != 'DST']

# combining draftkings and stats dfs
combo_raw = pd.merge_ordered(stats, dk_players, on='Name')

# getting rid of players who aren't playing
combo_raw = combo_raw[combo_raw.Salary.notnull()]

# renaming merged dataframe
combo = combo_raw

# finding positions
qb_raw = combo[combo['FantPos'] == 'QB']
wr_raw = combo[combo['FantPos'] == 'WR']
rb_raw = combo[combo['FantPos'] == 'RB']
te_raw = combo[combo['FantPos'] == 'TE']
flex_raw = combo[(combo['FantPos'] == 'RB') | (
    combo['FantPos'] == 'WR') | (combo['FantPos'] == 'TE')]

# finding wr by targets
wr_targets = wr_raw.Tgt.quantile(q=.75)

wr = wr_raw[(wr_raw['Tgt'] >= wr_targets) & (combo['VBD'] > 2)]

# finding rb by rushing attempts
rb_attempts = rb_raw.Att.quantile(q=.75)

rb = rb_raw[(rb_raw['Att'] >= rb_attempts) & (rb_raw['VBD'] > 1.5)]

# finding qb by Pass_cmp/Pass_Att and Pass_Yds/Pass_Att
cmp_per = qb_raw['Pass_Cmp']/qb_raw['Pass_Att']
pypa = qb_raw['Pass_Yds']/qb_raw['Pass_Att']  # pypa = pass yards per attempt
qb = qb_raw[(cmp_per > .6) & (pypa > 5) & (
    qb_raw['VBD'] > 2)]  # bitwise AND

# finding te by targets
te_targets = wr_raw.Tgt.quantile(q=.75)

te = te_raw[(te_raw['Tgt'] >= te_targets) & (te_raw['VBD'] > 2)]

# finding flex by combination
flex_targets = flex_raw.Tgt.quantile(q=.75)
flex_attempts = flex_raw.Att.quantile(q=.75)
flex = flex_raw[((flex_raw['Tgt'] >= flex_targets) | (
    flex_raw['Att'] >= flex_attempts)) & (flex_raw['VBD'] > 2)]

# finding defense by average fantasy points
d_arg = dk_def.AvgPointsPerGame.quantile(q=.25)
defense = dk_def[dk_def['AvgPointsPerGame'] >= d_arg]

# getting team ranges
qbrng = random.randint(0, len(qb)-1)
rbrng = random.randint(0, len(rb)-1)
rbrng2 = random.randint(0, len(rb)-1)
wrrng = random.randint(0, len(wr)-1)
wrrng2 = random.randint(0, len(wr)-1)
wrrng3 = random.randint(0, len(wr)-1)
terng = random.randint(0, len(te)-1)
flexrng = random.randint(0, len(flex)-1)
defenserng = random.randint(0, len(defense)-1)

# shuffling repeat positions to avoid duplicates, using pd.sample
rb1 = rb.sample(frac=1)
rb2 = rb.sample(frac=1)
wr1 = wr.sample(frac=1)
wr2 = wr.sample(frac=1)
wr3 = wr.sample(frac=1)

# making the team
team_raw = [qb.iloc[qbrng], rb1.iloc[rbrng], rb2.iloc[rbrng2], wr1.iloc[wrrng], wr2.iloc[wrrng2],
            wr3.iloc[wrrng3], te.iloc[terng], flex.iloc[flexrng], defense.iloc[defenserng]]
team = pd.DataFrame.from_records([x.to_dict() for x in team_raw])
