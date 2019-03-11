# import requests
# from bs4 import BeautifulSoup
# from lxml import html
# from lxml import etree

import pandas as pd
import sqlite3
import datetime
today_date = datetime.datetime.today().strftime('%Y-%m-%d')

from lineup_scraping import daily_lineups
import config

# Daily lineup fetch
gl = daily_lineups()
pull_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
lineups = pd.DataFrame.from_dict(gl.main())

# Add dates to dataframe
lineups['game_date'] = today_date
lineups['pull_time'] = pull_time

# Push dataframe to lineups database
con = sqlite3.connect(config.lineups_db_path)
lineups.to_sql(config.lineups_table, con, if_exists='append', index=False)
print('Daily Lineup Table Updated')