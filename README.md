# NFL DraftKings Lineup Generator
Lineup generator and web-scraper for draftkings lineups (NFL). :football:

- Uses [Pandas](https://pandas.pydata.org/), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), and [Requests](http://docs.python-requests.org/en/master/).


## how to use
- Fork and clone.
- Create your dotenv file.
    - Add the url of the offensive and defensive websites that will be scraped as variables.
- Add your draftkings .csv file to the csv_files directory.
    - Add the csv file name to your dotenv file as a variable.
- `print(lineup)` from the lineup_generator.py to get your draftkings lineup.

## sample .env file
```
defense_url=https://www.defensive-stats-site-to-be-scraped.com
offense_url=https://www.offensive-stats-site-to-be-scraped.com
csv=dk.csv
```

## authors
- Sawyer Zincone -_intial work_- [szincone](https://github.com/szincone) :clubs:

## license
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](https://github.com/szincone/nfl_dk_line_up/blob/08fb018deaaf21b3154d28d1ede2c9e466d8aa50/LICENSE.md) file for details.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)