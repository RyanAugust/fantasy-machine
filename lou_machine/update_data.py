import pandas as pd
import sqlite3
import datetime
import requests
import zipfile
from io import StringIO
import subprocess

from lou_machine import config
from lou_machine import data_ops

class update_data(object):
	def __init__(self):
		pass

	def main(self):
		start = datetime.datetime.now()
		print('Beginning Update: {}'.format(start.strftime('%Y-%m-%d %H:%M')))
		self.update_lineups()
		self.update_eventdata()
		end = datetime.datetime.now()
		return 'Update Completed in {}'.format((end-start).strftime('%H:%M:%S'))

	def update_lineups(self):
		# Daily lineup fetch
		gl = data_ops.scraping.daily_lineups()
		today_date = datetime.datetime.today().strftime('%Y-%m-%d')
		pull_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		lineups = pd.DataFrame.from_dict(gl.main()).drop_duplicates()

		# Add dates to dataframe
		lineups['game_date'] = today_date
		lineups['pull_time'] = pull_time

		# Correct Teams
		lineups['team'] = lineups['team'].replace('LAA','ANA')

		# Push dataframe to lineups database
		con = sqlite3.connect(config.players_db_path)
		lineups.to_sql(config.lineups_table, con, if_exists='append', index=False)
		con.close()
		print('Daily Lineup Table Updated')

	def update_eventdata(self):
		current_year = datetime.datetime.now().strftime('%Y')
		self.download_eventfiles(current_year=current_year)
		df = self.convert_raw_eventfiles(current_year=current_year)

	def convert_raw_eventfiles(self, current_year):
		bash_command = "wine data/temp/bevent -y {} -f 0-96 data/temp/{}???.EV? > data/temp/merged.csv".format(current_year,
																						current_year) ## Fix Pathing
		subprocess.call(bash_command, shell=True)
		df = pd.read_csv("{}/merged.csv".format()) ## Fix Pathing
		return df

	def download_eventfiles(self, current_year):
		base_url = 'https://www.retrosheet.org/events/{current_year}eve.zip'
		req_url = base_url.format(current_year=current_year)
		r = requests.get(req_url, config.temp_data_dir)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(config.temp_data_dir)
		return 0

	def check_missing_games(self, current_year):
		con = sqlite3.connect(config.mlb_db_path)
		query = """SELECT DISTINCT gameid FROM {} WHERE gameid like '%{}%'""".format(config.mlb_event_table,
																				current_year),
		existing_gids = pd.read_sql_query(query ,con)
		pd.read_
		
	def update_mapping(self):
		# Fetch remote player id mapping
		name_map_url = "http://crunchtimebaseball.com/master.csv"
		name_map_content = requests.get(name_map_url).content.decode('utf-8','ignore')
		name_map = pd.read_csv(StringIO(name_map_content))

		# Connect and compare updated id map with existing local map
		con = sqlite3.connect(config.player_mapping_db)
		try:
			existing_players = pd.read_sql('select * from {}'.format(config.player_map_table), con=con)
			final_map = existing_players.append(name_map).drop_duplicates()
		except:
			final_map = name_map

		# Push final mapping back to local db
		final_map.to_sql(con=con, name=config.player_map_table, if_exists='replace', index=False)
		# confirm and close
		con.close()
		print("Player ID's updated")

	def update_depthchart(self):
		dc_list = data_ops.scraping.update_depthchart()
		depth_chart = pd.DataFrame.from_dict(dc_list)
		depth_chart['pull_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		con = sqlite3.connect(config.players_db_path)
		depth_chart.to_sql(config.depthchart_table, con, if_exists='append', index=False)
		con.close()
		print('Team Depth Charts updated')

import sqlite3
import pandas

class import_data(object):
	def __init__(self):
		self.base_query = "SELECT {columns} FROM {table}"
		self.player_id_cols =["mlb_name","mlb_id","rotowire_name","rotowire_id",
							  "retro_name","rotowire_pos","retro_id"]
		self.current_year_condition = {"WHERE":{"gameid":{"like":"'%2018%'"}},
										"OR":{"gameid":{"like":"'%2017%'"}}}
	@staticmethod
	def _add_conditions(condition_dict: dict):
		condition_string = """"""
		for k, v in condition_dict.items():
			condition_string += str(k.upper()) + " "
			condition_string += str(list(v.keys())[0]) + " "
			condition_string += str(list(list(v.values())[0].keys())[0]) + " "
			condition_string += str(list(list(v.values())[0].values())[0]) + "\n"
		return condition_string

	@staticmethod
	def _structure_cols(columns: list):
		column_string = ",".join(columns)
		return column_string

	def make_connection(self, db):
		con = sqlite3.connect(db)
		return con

	def get_data(self, db, table, cols="*" ,condition_dict=None):
		if cols != "*":
			cols = self._structure_cols(cols)
		q = self.base_query.format(columns=cols, table=table)
		
		if condition_dict != None:
			condition_string = self._add_conditions(condition_dict)
			q += " " + condition_string
		con = self.make_connection(db)
		df = pandas.read_sql_query(sql=q, con=con)
		con.close()
		return df
