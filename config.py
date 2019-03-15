import os
user = os.environ['USER']

# PATHS
## Game/Event Data
mlb_data_path = os.getcwd() + "/data/baseball_data"
mlb_db_path = os.getcwd() + "/data/bevent.db"

## Lineups
lineups_db_path = os.getcwd() + "/data/lineups.db"
lineups_table = 'daily_lineups'

## ID mapping
player_mapping_db = os.getcwd() + "/data/playerid.db"
player_map_table = 'playerid_map'