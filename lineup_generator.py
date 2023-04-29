#! python
# combo_lineup.py - uses combined dataframes to generate draftkings lineup
from combiner import combo, dk_def
import os
import sys
import random
import pandas as pd

# finding positions
qb_raw = combo[combo['FantPos'] == 'QB']
wr_raw = combo[combo['FantPos'] == 'WR']
rb_raw = combo[combo['FantPos'] == 'RB']
te_raw = combo[combo['FantPos'] == 'TE']
flex_raw = combo[(combo['FantPos'] == 'RB') | (
    combo['FantPos'] == 'WR') | (combo['FantPos'] == 'TE')]

# getting team ranges
qbrng = random.randint(0, len(qb_raw)-1)
rbrng = random.randint(0, len(rb_raw)-1)
rbrng2 = random.randint(0, len(rb_raw)-1)
wrrng = random.randint(0, len(wr_raw)-1)
wrrng2 = random.randint(0, len(wr_raw)-1)
wrrng3 = random.randint(0, len(wr_raw)-1)
terng = random.randint(0, len(te_raw)-1)
flexrng = random.randint(0, len(flex_raw)-1)
defenserng = random.randint(0, len(dk_def)-1)

# shuffling repeat positions to avoid duplicates, using pd.sample
rb1_raw = rb_raw.sample(frac=1)
rb2_raw = rb_raw.sample(frac=1)
wr1_raw = wr_raw.sample(frac=1)
wr2_raw = wr_raw.sample(frac=1)
wr3_raw = wr_raw.sample(frac=1)

# making the team
team_raw = [qb_raw.iloc[qbrng], rb1_raw.iloc[rbrng], rb2_raw.iloc[rbrng2], wr1_raw.iloc[wrrng],
            wr2_raw.iloc[wrrng2], wr3_raw.iloc[wrrng3], te_raw.iloc[terng], flex_raw.iloc[flexrng], dk_def.iloc[defenserng]]
lineup = pd.DataFrame.from_records([x.to_dict() for x in team_raw])

def print_lineup():
    print(lineup)
