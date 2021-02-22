from stat_metrics import mlb_stat_metrics

class f_scoring(mlb_stat_metrics):
    def __init__(self, data, site='FD'):
        self.df = data
        try:
            self.b_scoring_matrix = pd.read_excel(config.f_scoring, sheet_name='batter')
            self.p_scoring_matrix = pd.read_excel(config.f_scoring, sheet_name='pitcher')
        except:
            print('no scoring matrix file')
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

    def get_batter_scoring_v2(self, df, groupby, player_ids=[], position='batter', work_columns=False):
        needed_cols = ['_1b','_2b','_3b','_hr','_bb','_hbp','_rbi']
        if len(player_ids) > 0:
            df = self.player_df(player_ids=player_ids, stat_type=position)
        if self.needed_col_check(needed_cols, df.columns.tolist()) == False:
            df_ = df.groupby(groupby).agg({'eventtype':[self._1b,self._2b,self._3b,self._hr,self._hbp,self._bb],
                                           'rbionplay':[self._rbi]})
            df_.columns = df_.columns.droplevel(0).tolist()
        else:
            df_ = df.groupby(groupby).sum()
        sm = self._filter_scoring_matrix(bat_pitch='batter')
        df_['f_score'] = (df_[['_1b','_2b','_3b','_hr','_bb','_hbp','_rbi']
                    ]*[sm['Single'],sm['Double'],sm['Triple'],
                       sm['Home Run'],sm['Walk'],sm['Walk'],sm['RBI']]).sum(axis=1)
        return_val = df_ if work_columns else df_[['f_score']]
        return return_val

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