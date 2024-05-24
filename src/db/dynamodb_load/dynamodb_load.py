import os
import sys
import boto3
from sqlalchemy import create_engine, text
from botocore.exceptions import ClientError
from decimal import Decimal

utils_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utilities'))
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
    print(utils_dir)

from db_helpers import get_aws_secrets
    
secrets = get_aws_secrets('rds_secrets', 'eu-west-2')
USERNAME = secrets['username']
PASSWORD = secrets['password']
HOST = secrets['host']
PORT = '5432'  

# Database connection URL
DATABASE_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"

# AWS DynamoDB and RDS configuration
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

def load_player_points_preds_to_dynamo():
    DYNAMODB_TABLE_NAME = "player_points_predictions"
    RDS_QUERY = """
    SELECT      element,
                player_name, 
                team_name,
                position,
                round,
                value,
                total_points_cum,
                predicted_points_n3r
    FROM        player_points_predictions
    ;"""
    
    # Connect to your database
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        # Execute raw SQL query directly
        result = connection.execute(text(RDS_QUERY))
        
        for row in result:
            element, player_name, team_name, position, round, value, total_points_cum, predicted_points_n3r = row
            
            # Insert data into DynamoDB
            dynamodb.Table(DYNAMODB_TABLE_NAME).put_item(
                Item={
                    'element': element,
                    'player_name': player_name,
                    'team_name': team_name,
                    'position': position,
                    'round': round,
                    'value': value,
                    'total_points_cum': total_points_cum,
                    'predicted_points_n3r': Decimal(str(predicted_points_n3r))
                }
            )

    print("Data transfer completed successfully.")
    
if __name__ == "__main__":
    load_player_points_preds_to_dynamo()