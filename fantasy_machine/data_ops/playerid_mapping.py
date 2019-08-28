import pandas as pd
import requests
from io import StringIO
import sqlite3

from fantasy_machine import config

def update_mapping():
	# Fetch remote player id mapping
	name_map_url = "http://crunchtimebaseball.com/master.csv"
	name_map_content = requests.get(name_map_url).content.decode('utf-8','ignore')
	name_map = pd.read_csv(StringIO(name_map_content))

	# Connect and compare updated id map with existing local map
	con = sqlite3.connect(config.player_mapping_db)
	existing_players = pd.read_sql('select * from {}'.format(config.player_map_table), con=con)
	final_map = existing_players.append(name_map).drop_duplicates()

	# Push final mapping back to local db
	final_map.to_sql(con=con, name=config.player_map_table, if_exists='replace', index=False)
	# confirm and close
	con.close()
	print("Player ID's updated")