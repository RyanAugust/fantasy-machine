import os
user = os.environ['USER']
# lou_machine_dir = '/'.join(os.getcwd().split('/')[:-1])
lou_machine_dir = os.getcwd()

# PATHS
## Temp dirs
temp_data_dir = "./data/temp"

## Game/Event Data
mlb_data_path = lou_machine_dir + "/data/baseball_data"
mlb_db_path = lou_machine_dir + "/data/bevent.db"
mlb_event_table = 'bevent'

## Lineups
lineups_db_path = lou_machine_dir + "/data/lineups.db"
lineups_table = 'daily_lineups'

## ID mapping
player_mapping_db = lou_machine_dir + "/data/playerid.db"
player_map_table = 'playerid_map'