class team_model(object):
    def __init__(self, lineups, data):
        self.fixture_lineup = lineups
        self.data = data
        self.team0, self.team1 = self.determine_teams(lineups['team'])
        self.team0_sp = self.find_starting_pitcher(lineup=lineups, team=self.team0)
        self.team1_sp = self.find_starting_pitcher(lineup=lineups, team=self.team1)
        self.team0_batters = self.find_batters(lineup=lineups, team=self.team0)
        self.team1_batters = self.find_batters(lineup=lineups, team=self.team1)
        
    def determine_teams(self, lineup_series):
        assert len(set(lineup_series)) == 2, "lineup contains more than 2 teams!"
        return set(lineup_series)
    
    def find_starting_pitcher(self, lineup, team):
        pitcher_id = lineup[(lineup['team'] == team) & (lineup['position'] == 'P')]['retro_id'].tolist()
        assert len(pitcher_id) == 1, "Multiple starting pitchers found"
        return pitcher_id[0]
    
    def find_batters(self, lineup, team):
        batter_ids = lineup[(lineup['team'] == team) & (lineup['position'] != 'P')]['retro_id'].tolist()
        assert len(batter_ids) in [8,9,10], "Too many players in starting lineup"
        return batter_ids
    
    def batter_dict(self, batters, pitcher=None):
        groupby = ['batter'] if pitcher != None else ['batter','pitcher']
        batter_wRAA = calc.calculate_v2(df=self.data,
                                        groupby=groupby, 
                                        position='batter',
                                        player_ids=batters,
                                        metric='wRAA')
        return batter_wRAA

"""
from lou_machine import update_data, import_data
from lou_machine import config
from lou_machine import stats
from lou_machine import model

import pandas as pd
import sqlite3

import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
# %matplotlib inline

import warnings
warnings.filterwarnings('ignore')

# # Update lineups
# update_data.update_lineups()
# # ud.update_mapping()
# update_data.update_depthchart()

bullpen_dc = {"WHERE":{"pull_time":{"=":"(SELECT MAX(pull_time) FROM {table})".format(
              table=config.depthchart_table)}},"AND":{"position":{"=":"'BULLPEN'"}}}
abr = import_data.get_data(db=config.id_mapping_db, 
                    table=config.team_abr_table)                 # team abr table
lineups = import_data.get_data(db=config.players_db_path,
                        table=config.lineups_table,
                        condition_dict={"WHERE":{"pull_time":{"=":"(SELECT MAX(pull_time) FROM {table})".format(
              table=config.lineups_table)}}})              # lineup table
player_map = import_data.get_data(db=config.id_mapping_db,
                           table=config.player_map_table,
                           cols=import_data.player_id_cols)             # playerid table
lineups_plus = lineups.merge(player_map,left_on=['player_id'],
                             right_on=['rotowire_id'],how='left')
dc = import_data.get_data(db=config.players_db_path,
                   table=config.depthchart_table,
                   condition_dict=bullpen_dc)                    # Bullpen table
bp_ids = dc.merge(player_map,left_on=['player_id'],
                 right_on=['mlb_id'],how='left')

event = import_data.get_data(db=config.mlb_db_path,
                     table=config.mlb_event_table,
                     condition_dict={'WHERE':import_data.current_year_condition['WHERE']}) # Event Data

calc = stats.baseball_stats.metric_calculator(data=event)

##############################################################################################

class team_model(object):
    def __init__(self, lineups, data):
        self.fixture_lineup = lineups
        self.data = data
        self.team0, self.team1 = self.determine_teams(lineups['team'])
        self.team0_sp = self.find_starting_pitcher(lineup=lineups, team=self.team0)
        self.team1_sp = self.find_starting_pitcher(lineup=lineups, team=self.team1)
        self.team0_batters = self.find_batters(lineup=lineups, team=self.team0)
        self.team1_batters = self.find_batters(lineup=lineups, team=self.team1)
        
    def determine_teams(self, lineup_series):
        assert len(set(lineup_series)) == 2, "lineup contains more than 2 teams!"
        return set(lineup_series)
    
    def find_starting_pitcher(self, lineup, team):
        pitcher_id = lineup[(lineup['team'] == team) & (lineup['position'] == 'P')]['retro_id'].tolist()
        assert len(pitcher_id) == 1, "Multiple starting pitchers found"
        return pitcher_id[0]
    
    def find_batters(self, lineup, team):
        batter_ids = lineup[(lineup['team'] == team) & (lineup['position'] != 'P')]['retro_id'].tolist()
        assert len(batter_ids) in [8,9,10], "Too many players in starting lineup"
        return batter_ids
    
    def batter_dict(self, batters, pitcher=None):
        groupby = ['batter'] if pitcher != None else ['batter','pitcher']
        batter_wRAA = calc.calculate_v2(df=self.data,
                                        groupby=groupby, 
                                        position='batter',
                                        player_ids=batters,
                                        metric='wRAA')
        return batter_wRAA

# model = team_model(lineups=lineups_plus[lineups_plus['fixture'] == 1], data=event)

"""