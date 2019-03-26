# import os
# user = os.environ['USER']
# lou_machine_dir = '/'.join(os.getcwd().split('/')[:-1])
# lou_machine_dir = os.getcwd()

# PATHS
## Temp dirs
temp_data_dir = "./data/temp"

## Game/Event Data
mlb_data_path = "./data/baseball_data"
mlb_db_path = "./data/bevent.db"
mlb_event_table = 'bevent'

## Players
players_db_path = "./data/players.db"
lineups_table = 'daily_lineups'
roster_table = 'team_rosters'
depthchart_table = 'depth_charts'

## ID mapping
player_mapping_db = "./data/playerid.db"
player_map_table = 'playerid_map'
team_abr_table = 'teamabr_map'

## Fantasy Scoring Matrix
f_scoring = "./data/fscoring.xlsx"