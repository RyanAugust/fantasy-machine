import os
user = os.environ['USER']
lou_machine_dir = '/'.join(os.getcwd().split('/')[:-2])

# PATHS
## Game/Event Data
mlb_data_path = lou_machine_dir + "/data/baseball_data"
mlb_db_path = lou_machine_dir + "/data/bevent.db"

## Lineups
lineups_db_path = lou_machine_dir + "/data/lineups.db"
lineups_table = 'daily_lineups'

## ID mapping
player_mapping_db = lou_machine_dir + "/data/playerid.db"
player_map_table = 'playerid_map'