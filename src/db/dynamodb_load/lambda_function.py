from dynamodb_load import load_player_points_preds_to_dynamo

def lambda_handler(event, context):
    load_player_points_preds_to_dynamo()