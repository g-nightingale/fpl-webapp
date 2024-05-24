import boto3
from decimal import Decimal
import json

def convert_decimals(obj):
    """Recursively convert Decimal objects to int or float."""
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        # Convert to int if no decimal places, float otherwise
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj


def get_data_from_dynamo_db(table_name, region_name='eu-west-2'):

    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name=region_name)

    # Reference your DynamoDB table
    table = dynamodb.Table(table_name)

    results_list = list()

    try:
        # Scan the table
        response = table.scan()

        # Access the items
        items = response['Items']
        print("Items in the table:")
        for item in items:
            # print(item)
            results_list.append(item)

        # Handle pagination if the table is large
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

    except Exception as e:
        print(f"Error scanning table: {str(e)}")

    # Convert Decimals in the retrieved items
    converted_results = convert_decimals(results_list)
    return converted_results

if __name__ == '__main__':
    TABLE_NAME = 'player_points_predictions'
    results_list = get_data_from_dynamo_db(TABLE_NAME, region_name='eu-west-2')
    print(results_list)