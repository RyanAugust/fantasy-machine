import requests
from bs4 import BeautifulSoup
from lxml import html
from lxml import etree

class daily_lineups(object):
    def __init__(self):
        self.lineup_url = 'https://www.rotowire.com/baseball/daily_lineups.htm'
        self.page = requests.get(self.lineup_url)
        self.tree = html.fromstring(self.page.content)
        self.info_locations = {'team':"//div[@class='lineup is-mlb'][{}]/div[2]/div/div/div[{}]/div[1]",
                               'pitcher':"//div[@class='lineup is-mlb'][{}]/div[2]/div[2]/ul[{}]/li[1]/div/a",
                               'players':"//div[@class='lineup is-mlb'][{}]/div[2]/div[2]/ul[{}]/li/a",
                               'positions':"//div[@class='lineup is-mlb'][{}]/div[2]/div[2]/ul[{}]/li/div[@class='lineup__pos']"}
    def main(self):
        games = []
        games_today = len(self.tree.xpath("//div[@class='lineup is-mlb']"))
        teams = [1,2]
        for game_num in range(games_today):
            game_num = game_num + 1
            game = []
            for team in teams:
                team_temp = self.tree.xpath(self.info_locations['team'].format(game_num,team))
                pitcher_temp = self.tree.xpath(self.info_locations['pitcher'].format(game_num,team))
                position_temp = self.tree.xpath(self.info_locations['positions'].format(game_num,team))
                player_temp = self.tree.xpath(self.info_locations['players'].format(game_num,team))
                game += self.get_players(player_temp, position_temp, team_temp, pitcher_temp, game_num)
            games += game
        return games
        

    def get_team(self, team_scrape):
        team = team_scrape[0].text
        return team
    def get_pitcher(self, pitcher_scrape):
        pitcher = pitcher_scrape[0].text
        return pitcher
    def get_players(self, players_scrape, position_scrape, team_scrape, pitcher_scrape, game_num):
        team = self.get_team(team_scrape)
        player_list = []
        pitcher = self.get_pitcher(pitcher_scrape)
        player_list.append({'fixture':game_num,
                                'name':pitcher,
                                'position':'P',
                                'team':team})
        for player_, position_ in zip(players_scrape, position_scrape):
            position = position_.text
            player_name = player_.attrib['title']
            player_list.append({'fixture':game_num,
                                'name':player_name,
                                'position':position,
                                'team':team})
        return player_list