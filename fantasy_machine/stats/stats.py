import pandas as pd
from fantasy_machine import config
import sqlite3
from .stat_metrics import mlb_stat_metrics, nfl_stat_metrics, f_scoring

class metric_calculator(object):
    def __init__(self, data, stat_metrics, ):
        self.mts = stat_metrics(data)

        self.fs = f_scoring(data)
        self.metric_fxns = self.mts.metric_fxns
            
    def calculate(self, player_ids, metric):
        """Pass a list of `player_ids` and a `metric` to be calculated
        Metrics are checked against a set of available functions"""
        self.metric_exists(metric)
        metric_calc = self.metric_fxns[metric]
        value = metric_calc(player_ids)
        return value

    def calculate_v2(self, df, groupby, metric, position='batter', player_ids=[], work_columns=False):
        """"""
        self.metric_exists(metric)
        metric_calc = self.metric_fxns[metric]
        return_val = metric_calc(df=df, groupby=groupby, position=position, player_ids=player_ids, work_columns=work_columns)
        return return_val
        
    def metric_exists(self, metric):
        assert metric in self.metric_fxns.keys(), "Invalid metric, metric not defined"
        return None