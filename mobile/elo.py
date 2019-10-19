import numpy as np

class ELO_management(object):
    def __init__(self):
        self.member_elo_cache = {}
        self.starting_elo = 1600

    def update_elo(self, member, new_elo):
        self.cache_checker(member)
        """Is this the intended functionality? This would be a situation where you're checking for
        the presence of a member and in the event that member isn't in the cache default value 
        would be applied, you would then come to the next line and be applying a new elo socre to
        them thus overrideing the default value placement"""
        self.member_elo_cache[member] = new_elo
        return 0

    # def calculate_elo(self, member1, member2):
    #     cached_scores = self.fetch_elos(member1, member2)

    def fetch_elo(self, member):
        """return `member1` and `member2` elo scores from the class cache.
        integrety check is completed by `cache_checker` to ensure members are available"""
        self.cache_checker(member)
        return self.member_elo_cache[member]

    def cache_checker(self, member):
        """Ensure that every member passed is either present in the cache with an active elo score.
        In the event a member is not in the cache calls `new_member` to update cache"""
        if member not in self.member_elo_cache.keys():
            self.new_member(member)
        return 0

    def new_member(self, member):
        """ When passed a member, adds the member to the cache of members using the default starting
        elo value, referenced from `self.starting_elo`"""
        self.member_elo_cache.update({member:self.starting_elo})
        return 0

    def show_cache(self):
        print(self.member_elo_cache)


class ELO(object):
    def __init__(self, K=32, score_div_factor=2, reset_factor=2, member_list=[]):
        self.EM = ELO_management()
        self.K = K
        self.score_div_factor = score_div_factor
        if len(member_list) > 0:
            [self.EM.new_member(member) for member in member_list]
        self.reset_factor = reset_factor
        
    def reset_function(self, member_elo_dict):
        """The reset function that is employed for resets. This can be overridden based on settings
        that you'd like to apply to the global elo's of members when there is some form of reset in
        play. This function is executed by this classes `season_reset` function."""
        for member in member_elo_dict.keys():
            current_elo = member_elo_dict[member]
            new_elo = current_elo + (self.EM.starting_elo - current_elo) / self.reset_factor
            member_elo_dict[member] = new_elo
        return member_elo_dict

    @staticmethod
    def get_win_probibility(member1_elo, member2_elo):
        """Compute the head to head win probilbility for each member."""
        member1_w_prob = (1.0 / (1.0 + 10**((member2_elo - member1_elo) / 400)))
        member2_w_prob = (1.0 / (1.0 + 10**((member1_elo - member2_elo) / 400)))

        return member1_w_prob, member2_w_prob

    def do_competition(self, winner, loser, scoring={}):
        """Retriesve each of the members current elo ratings by using the ELO_management class.
        Then apply new ratings based on which member has won"""
        winner_elo = self.EM.fetch_elo(winner)
        loser_elo = self.EM.fetch_elo(loser)
        winner_w_prob, loser_w_prob = self.get_win_probibility(winner_elo, loser_elo)
        
        win_score, lose_score = self.scoring_function(winner_w_prob, loser_w_prob, scoring)
        winner_new_elo = winner_elo + win_score
        loser_new_elo = loser_elo + lose_score
        
        if loser_new_elo < 0:
            loser_new_elo = 0

        self.EM.update_elo(winner, winner_new_elo)
        self.EM.update_elo(loser, loser_new_elo)
        return winner_w_prob, loser_w_prob

    def scoring_function(self, winner_w_prob, loser_w_prob, scoring):
        if 'win_score' and 'lose_score' in scoring.keys():
            w_score, l_score = scoring['win_score'], scoring['lose_score']
            score_differential = w_score-l_score
            if score_differential < 1:
                return 0, 0
            else:
                score_factor = np.log(score_differential) / self.score_div_factor
        else:
            score_factor = 1
            
        win_score = self.K * (1 - winner_w_prob) * score_factor
        lose_score = self.K * (0 - loser_w_prob) * score_factor
        
        return win_score, lose_score
        
    
    def add_members(self, member_list):
        for member in member_list:
            self.EM.new_member(member)
        return winner_w_prob, loser_w_prob
    
    def season_reset(self):
        """Resets the playing field by implementing the `self.reset_function` against the entire
        cache of members managed by `self.EM`"""
        self.EM.member_elo_cache = self.reset_function(self.EM.member_elo_cache)
        return 0