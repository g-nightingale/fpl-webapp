from transform import create_player_static_data, create_transformed_team_data, \
    create_transformed_player_history_data, create_modelling_data

def lambda_handler(event, context):
    create_player_static_data()
    create_transformed_team_data()
    create_transformed_player_history_data()
    create_modelling_data()