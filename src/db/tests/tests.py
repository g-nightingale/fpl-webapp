import requests
import json
import os
import sys

utils_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utilities'))
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
    print(utils_dir)

from db_helpers import create_table_if_not_exists, truncate_table, drop_table, store_data_in_rds, run_query
    

def check_table_counts():
    """
    Check the table counts.
    """

    print(f'raw_fixtures row count: {run_query("SELECT COUNT(*) FROM raw_fixtures")}')
    print(f'raw_element_types row count: {run_query("SELECT COUNT(*) FROM raw_element_types")}')
    print(f'raw_teams row count: {run_query("SELECT COUNT(*) FROM raw_teams")}')
    print(f'raw_player_static row count: {run_query("SELECT COUNT(*) FROM raw_player_static")}')
    print(f'raw_player_history row count: {run_query("SELECT COUNT(*) FROM raw_player_history")}')
    print(f'modelling_data row count: {run_query("SELECT COUNT(*) FROM modelling_data")}')

def drop_tables():
    """
    Drop all the tables.
    """

    drop_table('raw_fixtures')
    drop_table('raw_element_types')
    drop_table('raw_teams')
    drop_table('raw_player_static')
    drop_table('raw_player_history')

if __name__ == '__main__':
    check_table_counts()
    # drop_tables()
    run_query("SELECT * FROM raw_fixtures")