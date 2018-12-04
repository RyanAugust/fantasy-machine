import os
import requests, zipfile, io
import pandas as pd
import sqlite3

from config import mlb_data_path, mlb_db_path

class MLB_data_gather(object):
    def __inif__(self):
        pass

    def get_year(self, year, data_path=mlb_data_path):
        zip_file_url = "https://www.retrosheet.org/events/{}eve.zip".format(year)
        r = requests.get(zip_file_url, mlb_data_path)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(mlb_data_path)

    def parse_roster(self, year, roster_data):
        roster = []
        for i, line in enumerate(roster_data.split('\n')):
            line = line.replace('\r','')
            line_list = line.split(',')
            roster.append({'player_id':line_list[0],
                           'last_name':line_list[1],
                           'first_name':line_list[2],
                           'bats':line_list[3],
                           'throws':line_list[4],
                           'team':line_list[5],
                           'pos':line_list[6]})
            return roster
            
    def parse_game(self, game):
        info_dict = []
        roster_start_dict = []
        play_dict = []
        sub_dict = []
        data_dict = []
        adjustment_dict = []
        eventcount = 0
        for i, line in enumerate(game.split('\n')):
            if i == 0:
                game_id = line.replace('\r','')
            else:
                line = line.replace('\r','')
                line_list = line.split(',')
                line_id = line_list[0]
                if line_id == 'version':
                    version = line.split(',')[1]
                elif line_id == 'info':
                    info_dict.append({'field':line_list[1],
                                      'value':line_list[2]})
                elif line_id == 'start':
                    roster_start_dict.append({'player_id':line_list[1],
                                              'player_name':line_list[2].strip('"'),
                                              'team_HA':line_list[3],
                                              'batting_order':line_list[4],
                                              'position':line_list[5]})
                elif line_id == 'play':
                    play_dict.append({'eventcount':eventcount,
                                      'inning':line_list[1],
                                      'half':line_list[2],
                                      'player_id':line_list[3],
                                      'count':line_list[4],
                                      'pitches':line_list[5],
                                      'event':line_list[6]})
                    eventcount += 1
                elif line_id in ['bajd','pajd','ladj']:
                    adjustment_dict.append({'eventcount':eventcount,
                                           'event_type':line_id,
                                           'player_id':line_list[1],
                                           'adj':line_list[2]})
                elif line_id == 'sub':
                    sub_dict.append({'eventcount':eventcount,
                                     'player_id':line_list[1],
                                     'player_name':line_list[2].strip('"'),
                                     'team_HA':line_list[3],
                                     'batting_order':line_list[4],
                                     'position':line_list[5]})
                    eventcount += 1
                elif line_id == 'data':
                    data_dict.append({'field':line_list[1],
                                      'player_id':line_list[2],
                                      'er':line_list[3]})
                else:
                    pass
        game_dict = {'info':info_dict,
                     'starters':roster_start_dict,
                     'plays':play_dict,
                     'substitutions':sub_dict,
                     'game_data':data_dict,
                     'adjustment':adjustment_dict}
        return game_id, game_dict

    def parse_game_file(self, payload):
        conn = sqlite3.connect(os.getcwd() +"/data/MLB.db")
        dict_names = ['info','starters','plays','substitutions','game_data','adjustment']
        for game in payload.split('id,'):
            if len(game) > 1:
                game_id, game_dict = self.parse_game(game)
                for dict_name in dict_names:
                    if len(game_dict[dict_name]) > 0:
                        df = pd.DataFrame(game_dict[dict_name])
                        df['game_id'] = game_id
                        df.to_sql(dict_name,conn,if_exists="append",index=False)
                    else:
                        pass
            else:
                pass
        conn.close()
        return 'File Complete'

################################################################################
########################### REWRITE FOR ROSTER FILES ###########################
################################################################################
    def parse_roster_file(self, payload):
        conn = sqlite3.connect(os.getcwd() +"/data/MLB.db")
        dict_names = ['info','starters','plays','substitutions','game_data','adjustment']
        for game in payload.split('id,'):
            if len(game) > 1:
                game_id, game_dict = self.parse_game(game)
                for dict_name in dict_names:
                    if len(game_dict[dict_name]) > 0:
                        df = pd.DataFrame(game_dict[dict_name])
                        df['game_id'] = game_id
                        df.to_sql(dict_name,conn,if_exists="append",index=False)
                    else:
                        pass
            else:
                pass
        conn.close()
        return 'File Complete'
################################################################################
################################################################################
################################################################################

    def run_year(self, year, data_path=mlb_data_path):
        for a,b,c in os.walk(mlb_data_path):
            for eventfile in c:
                if '.EV' in eventfile:
                    if str(year) in eventfile:
                        with open(mlb_data_path + '/' + eventfile, 'r') as f:
                            data = f.read()
                            f.close()
                        self.parse_game_file(data)
                elif '.ROS' in eventfile:
                    if str(year) in eventfile:
                        with open(mlb_data_path + '/' + eventfile, 'r') as f:
                            data = f.read()
                            f.close()
                        self.parse_roster(year=year, roster_data=data)
                elif 'TEAM' in eventfile:
                    pass
                elif '.DS_S' in eventfile:
                    pass
                else:
                    print('UNUSED FILE: {}'.format(eventfile))
        print('{} Complete'.format(year))

    def main(self, years):
        for year in years:
            self.get_year(year=year)
            self.run_year(year=year)
        return "---Run Complete---"
