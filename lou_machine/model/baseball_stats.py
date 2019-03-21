import pandas as pd
from lou_machine import config

class metric_calculator(object):
    def __init__(self, data):
        self.mts = stat_metrics(data)
        self.fs = f_scoring(data)
        self.metric_fxns = {
            'BA':self.mts.batting_avg,
            'SLG':self.mts.slugging,
            'wOBA':self.mts.wOBA,
            'wRAA':self.mts.wRAA,
            'UZR':self.mts.UZR,
            'fWAR':self.mts.fWAR,
            ### Pitching
            'IP':self.mts.inning_pitched,
            'WHIP':self.mts.WHIP,
            'FIP':self.mts.FIP,
            'QS':self.mts.quality_start,
            'ER':self.mts.earned_runs,
            'pwin':self.mts.pitcher_win,
            }
            
    def calculate(self, player_ids, metric):
        self.metric_exists(metric)
        metric_calc = self.metric_fxns[metric]
        value = metric_calc(player_ids)
        return value
        
    def metric_exists(self, metric):
        assert metric in self.metric_fxns.keys(), "Invalid metric, metric not defined"
        return None

class stat_metrics(object):
    def __init__(self, data):
        self.df = data
        self.fg_constants = {'wOBA':.315,
                        'wOBAScale':1.226,
                        'wBB':.690,
                        'wHBP':.720,
                        'w1B':.880,
                        'w2B':1.247,
                        'w3B':1.578,
                        'wHR':2.031,
                        'cFIP':3.161}
        self.position_adj = {1:0,
            2:+12.5,
            3:-12.5,
            4:+2.5,
            6:+7.5,
            5:+2.5,
            7:-7.5,
            8:+2.5,
            9:-7.5,
            10:-17.5}
        
    def pre_process(self, df, process_dict):
#         event_specs =  pd.DataFrame(
#             index=np.arange(26)
#             ).join(df.groupby('eventtype').agg(process_dict)).fillna(0)
        event_specs = df.groupby('eventtype').agg(process_dict)
        event_specs = self.check_eventtype(event_specs)
        return event_specs
    
    def check_eventtype(self,df):
        for num in range(26):
            if num not in df.index:
                df.loc[num] = 0.0
            else:
                pass
        return df
    
    def player_df(self, player_ids, stat_type='batter'):
        if type(player_ids) == str:
            player_ids = [player_id]
        elif type(player_ids) == list:
            pass
        else:
            assert "Invalid Player ID/List"
        
        return self.df[self.df[stat_type].isin(player_ids)]
            
    #####################################
    ############ BATTING  ###############
    #####################################
    def batter_stolen_base(self, player_ids):
        sf = len(self.df[(self.df['sbfirst'] == "T") & (self.df['firstrunner'].isin(player_ids))])
        ss = len(self.df[(self.df['sbsecond'] == "T") & (self.df['secondrunner'].isin(player_ids))])
        st = len(self.df[(self.df['sbthird'] == "T") & (self.df['thirdrunner'].isin(player_ids))])
        value = sf + ss + st
        return value

    def batter_run_scored(self, player_ids):
        sf = len(self.df[(self.df['sbfirst'] == "T") & (self.df['firstrunner'].isin(player_ids))])
        ss = len(self.df[(self.df['sbsecond'] == "T") & (self.df['secondrunner'].isin(player_ids))])
        st = len(self.df[(self.df['sbthird'] == "T") & (self.df['thirdrunner'].isin(player_ids))])
        value = sf + ss + st
        return value

    def wOBA(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        ## General Stats
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        hbp = df_.loc[16]
        ibb = df_.loc[15]
        bb = df_.loc[14] + ibb
        b1 = df_.loc[20]
        b2 = df_.loc[21]
        b3 = df_.loc[22]
        hr = df_.loc[23]
        ab = len(df[df['abflag'] == 'T'])
        ibb = df_.loc[15]
        ## SF calculation
        sf = len(df[df['sfflag'] == 'T'])
        value = (
            (self.fg_constants['wBB']*(bb-ibb) + 
            self.fg_constants['wHBP']*hbp + 
            self.fg_constants['w1B']*b1 + 
            self.fg_constants['w2B']*b2 + 
            self.fg_constants['w3B']*b3 + 
            self.fg_constants['wHR']*hr)/
                (ab+bb-ibb+sf+hbp))
        return value
    
    def batting_avg(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        b1 = df_.loc[20]
        b2 = df_.loc[21]
        b3 = df_.loc[22]
        hr = df_.loc[23]
        ## AB flag count
        ab = len(df[df['abflag'] == 'T'])
        value = (b1+b2+b3+hr)/ab
        return value

    def slugging(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        b1 = df_.loc[20]
        b2 = df_.loc[21]
        b3 = df_.loc[22]
        hr = df_.loc[23]
        ## AB flag count
        ab = len(df[df['abflag'] == 'T'])
        value = (b1+(b2*2)+(b3*3)+(hr*4))/ab
        return value
    
    def wRAA(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        wOBA = self.wOBA(player_ids=player_ids)
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        ab = len(df[df['abflag'] == 'T'])
        hbp = df_.loc[16]
        ibb = df_.loc[15]
        bb = df_.loc[14] + ibb
        sh = len(df[df['shflag'] == 'T'])
        ## SF calculation
        sf = len(df[df['sfflag'] == 'T'])
        value = ((wOBA-self.fg_constants['wOBA'])/self.fg_constants['wOBAScale'])*(ab+bb+hbp+sf+sh)
        return value
    
    def UZR(self, player_ids): ########################################################################## Needs implementation
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        value = 0
        return value
    
    def position_determination(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        pos_group = df[['gameid','defensiveposition']].groupby('defensiveposition').count()
        position = pos_group.sort_values('gameid', ascending=False).index.tolist()[0]
        return position
    
    def fWAR(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        wRAA = self.wRAA(player_ids)
        UZR = self.UZR(player_ids)
        pos = self.position_determination(player_ids)
        position = self.position_adj[pos]
        pa = len(df)
        value = wRAA + 0 + position + (20/600)*pa ######################################################### Working
        return value
    #####################################
    ############ PITCHING  ##############
    #####################################
    def inning_pitched(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='pitcher')
        ip = float(df['outsonplay'].sum())/3.0
        return ip

    def WHIP(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='pitcher')
        ip = self.inning_pitched(player_ids)
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        b1 = df_.loc[20]
        b2 = df_.loc[21]
        b3 = df_.loc[22]
        hr = df_.loc[23]
        ibb = df_.loc[15]
        bb = df_.loc[14]
        value = ((bb + ibb) + (b1 + b2 + b3 + hr))/ip
        return value

    def FIP(self, player_ids):
        ip = self.inning_pitched(player_ids)
        df = self.player_df(player_ids=player_ids, stat_type='pitcher')
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        hr = df_.loc[23]
        bb = df_.loc[14]
        hbp = df_.loc[16]
        k = df_.loc[3]
        value =  (13*hr + 3*(hbp+bb) - 2*k)/ip + self.fg_constants['cFIP']
        return value

    def quality_start(self, player_ids):
        ### Started game
        ### Pitched 6 innings
        ### less than 3 ER
        value = 0
        return value

    def earned_runs(self, player_ids):
        value = 0
        return value

    def pitcher_win(self, player_ids):
        value = 0
        return value

class f_scoring(stat_metrics):
    def __init__(self, data, site='FD'):
        self.df = data
        self.b_scoring_matrix = pd.read_excel(config.f_scoring, sheet_name='batter')
        self.p_scoring_matrix = pd.read_excel(config.f_scoring, sheet_name='pitcher')
        self.site = site

    def _filter_scoring_matrix(self, bat_pitch):
        assert bat_pitch in ['batter','pitcher'], "Invalid scoring type designation. Pick from [batter,pitcher]"
        if bat_pitch == 'batter':
            scoring_matrix = self.b_scoring_matrix[self.site]
        elif bat_pitch == 'pitcher':
            scoring_matrix = self.p_scoring_matrix[self.site]
        else:
            print("ugh oh")
        return scoring_matrix

    def get_batter_scoring(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='batter')
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        sm = self._filter_scoring_matrix(bat_pitch='batter')
        b1 = df_.loc[20]
        b2 = df_.loc[21]
        b3 = df_.loc[22]
        hr = df_.loc[23]
        bb = df_.loc[14]
        hbp = df_.loc[16]
        rbi = df['rbionplay'].sum()
        rs = self.batter_run_scored(player_ids)
        sb = self.batter_stolen_base(player_ids)
        value = (b1*sm['Single'] + b2*sm['Double'] + b3*sm['Triple'] + hr*sm['Home Run'] +
                (bb+hbp)*sm['Walk'] + rbi*sm['RBI'] + rs*sm['Run Scored'] + sb*sm['Stolen Base'])
        return value

    def get_pitcher_scoring(self, player_ids):
        df = self.player_df(player_ids=player_ids, stat_type='pitcher')
        df_ = self.pre_process(df, {'gameid':'count'})['gameid']
        sm = self._filter_scoring_matrix(bat_pitch='pitcher')
        ip = self.inning_pitched(player_ids=player_ids)
        qs = self.quality_start(player_ids=player_ids)
        win = self.pitcher_win(player_ids=player_ids)
        er = self.earned_run(player_ids=player_ids)
        k = df_.loc[3]
        value = (ip*sm['IP'] + qs*sm['Quality Start'] + win*sm['Win'] +
                 er*sm['ER']  + k*sm['K'])