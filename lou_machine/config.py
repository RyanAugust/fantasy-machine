# import os
# user = os.environ['USER']
# lou_machine_dir = '/'.join(os.getcwd().split('/')[:-1])
# lou_machine_dir = os.getcwd()
base_path = '.'

# PATHS
## Temp dirs
temp_data_dir = "{base_path}/data/temp".format(base_path=base_path)

## Game/Event Data
mlb_data_path = "{base_path}/data/baseball_data".format(base_path=base_path)
mlb_db_path = "{base_path}/data/bevent.db".format(base_path=base_path)
mlb_event_table = 'bevent'

## Players
players_db_path = "{base_path}/data/players.db".format(base_path=base_path)
lineups_table = 'daily_lineups'
roster_table = 'team_rosters'
depthchart_table = 'depth_charts'

## ID mapping
id_mapping_db = "{base_path}/data/id_mapping.db".format(base_path=base_path)
player_map_table = 'playerid_map'
team_abr_table = 'teamabr_map'

## Fantasy Scoring Matrix
f_scoring = "{base_path}/data/fscoring.xlsx".format(base_path=base_path)