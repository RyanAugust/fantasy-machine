from local_config import stats_name_lookup

class statistics(object):
	def __init__(self, datasource, stats_name_lookup=stats_name_lookup):
		self.datasource = datasource
		self.stats_name_lookup = stats_name_lookup
	
