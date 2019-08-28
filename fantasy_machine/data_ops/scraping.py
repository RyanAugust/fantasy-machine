
class daily_lineups(object):
	def __init__(self):

		import requests
		from lxml import html, etree

		self.lineup_url = 'https://www.rotowire.com/baseball/daily_lineups.htm'
		self.page = requests.get(self.lineup_url)
		self.tree = html.fromstring(self.page.content)
		self.div_selection = "contains(@class,'lineup is-mlb') and not(contains(@class,'is-tools'))"
		self.info_locations = {'team':"//div[{}][{}]/div[2]/div/div/div[{}]/div[1]/text()",
							   'pitcher':"//div[{}][{}]/div[2]/div[2]/ul[{}]/li[1]/div/a",
							   'players':"//div[{}][{}]/div[2]/div[2]/ul[{}]/li/a",
							   'positions':"//div[{}][{}]/div[2]/div[2]/ul[{}]/li/div[@class='lineup__pos']",
							   'lineup_status':"//div[{}][{}]/div[2]/div[2]/ul[{}]/li[2]",
							   'lineup_odds':"//div[{}][{}]/div[2]/div[3]/div[2]/div[@class='lineup__odds']/div[1]/text()"}
	def main(self):
		games = []
		games_today = len(self.tree.xpath("//div[{}]".format(self.div_selection)))
		teams = [1,2]
		for game_num in range(games_today):
			game_num = game_num + 1
			game = []
			try:
				for team in teams:
					team_temp = self.tree.xpath(self.info_locations['team'].format(self.div_selection,game_num,team))
					pitcher_temp = self.tree.xpath(self.info_locations['pitcher'].format(self.div_selection,game_num,team))
					position_temp = self.tree.xpath(self.info_locations['positions'].format(self.div_selection,game_num,team))
					player_temp = self.tree.xpath(self.info_locations['players'].format(self.div_selection,game_num,team))
					lineup_status_temp = self.tree.xpath(self.info_locations['lineup_status'].format(self.div_selection,game_num,team))
					lineup_odds_temp = self.tree.xpath(self.info_locations['lineup_odds'].format(self.div_selection,game_num))
					game += self.get_players(player_temp, position_temp, team_temp, pitcher_temp, lineup_status_temp, game_num,lineup_odds_temp)
			except:
				pass
			games += game
		return games


	def get_team(self, team_scrape):
		try:
			team = team_scrape[0]
		except:
			team = None
		return team
	def get_pitcher(self, pitcher_scrape):
		pitcher = pitcher_scrape[0].text
		pitcher_id = int(pitcher_scrape[0].attrib['href'].split('?id=')[-1])
		return pitcher, pitcher_id
	def get_lineup_status(self, lineup_status_scrape):
		lineup_status_scrape_class = lineup_status_scrape[0].attrib['class']
		try:
			if 'confirmed' in lineup_status_scrape_class:
				lineup_status = 'Confirmed'
			elif 'expected' in lineup_status_scrape_class:
				lineup_status = 'Expected'
			else:
				lineup_status = 'None'
		except:
			print('status retrieval failure')
			lineup_status = 'None'
		return lineup_status

	def get_players(self, players_scrape, position_scrape, team_scrape, pitcher_scrape, lineup_status_scrape, game_num, lineup_odds_temp):
		team = self.get_team(team_scrape)
		player_list = []
		try:
			lineup_odds = ' '.join(lineup_odds_temp[0].split(' ')[1:])
		except:
			lineup_odds = ''
		lineup_status = self.get_lineup_status(lineup_status_scrape)
		pitcher, pitcher_id = self.get_pitcher(pitcher_scrape)
		player_list.append({'fixture':game_num,
								'player_name':pitcher,
								'player_id':pitcher_id,
								'position':'P',
								'team':team,
								'lineup_status':lineup_status,
								'lineup_odds':lineup_odds})
		for player_, position_ in zip(players_scrape, position_scrape):
			position = position_.text
			player_name = player_.attrib['title']
			player_id = int(player_.attrib['href'].split('?id=')[-1])
			player_list.append({'fixture':game_num,
								'player_name':player_name,
								'player_id':player_id,
								'position':position,
								'team':team,
								'lineup_status':lineup_status,
								'lineup_odds':lineup_odds})
		return player_list

def retrieve_past_salaries(years=None, weeks=None, site='FD'):
	import requests
	from lxml import html, etree

	base_url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week={week}&year={year}&game={site}&scsv=1'

	if years == None:
		years = range(2011,2019)
	if weeks == None:
		weeks = range(1,18)

	final_csv = []
	for year in years:
		for week in weeks:
			try:
				page = requests.get(base_url.format(week=week, year=year, site=site))
				tree = html.fromstring(page.content)
				csv = tree.xpath("//pre/text()")
				final_csv.append(csv) csv

			except:
				print('error pulling salaries for week {week}-{year} for {site}'.format(week=week, year=year, site=site))
	return final_csv

def update_depthchart():
	
	import requests
	from lxml import html, etree
	
	depth_charts = []
	base_url = 'http://oakland.athletics.mlb.com/team/depth_chart/?c_id={}'
	teams = ['oak','ana','hou','tor','atl','mil','stl','chc','ari','la','sf','cle','sea','mia','nym',
			'was','bal','sd','phi','pit','tex','tb','bos','cin','col','kc','det','min','cws','nyy']
	for team_name in teams:
		try:
			dc = requests.get(base_url.format(team_name))
			tree = html.fromstring(dc.content)
			team_dc = []
			team_page_dc = tree.xpath("//div[@id='depth_chart']")[0]
			positions = team_page_dc.xpath("div[contains(@id,'pos_')]")
			for position in positions:
				try:
					position_name = position.xpath("ul/li[@class='position_header']/text()")[0]
					players = []
					player_els = position.xpath("ul/li/a[@target='_blank']")
					for player in player_els:
						player_name = player.text
						player_id = int(player.attrib['href'].split('id=')[-1])
						player_dict = {'player_name':player_name,
									   'player_id':player_id,
									   'position':position_name,
									   'team_name':team_name.upper()}
						depth_charts.append(player_dict)
				except: # The final one on every page breaks. This acconts for that
					pass
		except:
			print(team_name)
	return depth_charts