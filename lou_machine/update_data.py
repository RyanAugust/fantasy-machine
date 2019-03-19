import pandas as pd
import sqlite3
import datetime
import requests
import zipfile
import io
import subprocess

from lou_machine import config
from data_ops import lineup_scraping
from data_ops import playerid_mapping

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
		from lou_machine import data_ops

		# Daily lineup fetch
		gl = data_ops.lineup_scraping.daily_lineups()
		today_date = datetime.datetime.today().strftime('%Y-%m-%d')
		pull_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		lineups = pd.DataFrame.from_dict(gl.main()).drop_duplicates()

		# Add dates to dataframe
		lineups['game_date'] = today_date
		lineups['pull_time'] = pull_time

		# Push dataframe to lineups database
		con = sqlite3.connect(config.lineups_db_path)
		lineups.to_sql(config.lineups_table, con, if_exists='append', index=False)
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

	def check_missing_games(self, current_year, ):
		con = sqlite3.connect(config.mlb_db_path)
		query = """SELECT DISTINCT gameid FROM {} WHERE gameid like '%{}%'""".format(config.mlb_event_table,
																				current_year),
		existing_gids = pd.read_sql_query(query ,con)
		pd.read_


