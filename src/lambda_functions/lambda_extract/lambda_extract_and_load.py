from extract_and_load import update_fixtures, update_element_types, update_teams, \
    update_player_data, update_player_historical_data

def lambda_handler(event, context):
    update_fixtures()
    update_element_types()
    update_teams()
    update_player_data()
    update_player_historical_data()