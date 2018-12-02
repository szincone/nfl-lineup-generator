# NFL DraftKings Lineup Generator
A web scraper that uses Beautiful Soup and Pandas to create your DraftKings lineups for you.

-Written in [Python](https://www.python.org/).

-Uses [Pandas](https://pandas.pydata.org/).

-Uses [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

## using the program
combo_linup.py takes a "stats" dataframe from scrape_fb_ref_off.py and a "defense" dataframe from scrape_fb_ref_def.py (both scrape pro-football-reference.com). combine_nfl_dfs.py then converts a spreadsheet from from DraftKings(not included) into a dataframe and imports, then merges, the previous 2 dataframes with our new "combo" dataframe. Now that we have our Offensive, Defensive, and DraftKings data, all merged and cleaned up, we use combo_linup.py to create a "team" dataframe that has our DraftKings lineup.

## authors
-Sawyer Zincone -_intial work_- [szincone](https://github.com/szincone)

## license
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE.md](https://github.com/szincone/nfl_dk_line_up/blob/08fb018deaaf21b3154d28d1ede2c9e466d8aa50/LICENSE.md) file for details.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
