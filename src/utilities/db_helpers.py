from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import pandas as pd
import json
import boto3
import datetime

def get_current_datetime():
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_datetime

def get_aws_secrets(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    # Decode the secret string
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def connect_rds(echo=False):
    # This function creates a connection to the RDS instance
    # Load environment variables from .env file
    # load_dotenv()

    # Database credentials and connection details
    # USERNAME = os.getenv('USERNAME')
    # PASSWORD = os.getenv('PASSWORD')
    # HOST = os.getenv('HOST')
    # PORT = '5432'  

    secrets = get_aws_secrets('rds_secrets', 'eu-west-2')
    USERNAME = secrets['username']
    PASSWORD = secrets['password']
    HOST = secrets['host']
    PORT = '5432'  

    # Database connection URL
    DATABASE_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    print(DATABASE_URL)

    # Create an engine instance
    engine = create_engine(DATABASE_URL, echo=echo)
    return engine

def print_error_msg(exception):
    print(f'ERROR: {exception}')

def create_table_if_not_exists(create_table_query):

    try:
        engine = connect_rds()  
        with engine.connect() as connection:
            connection.execute(text(create_table_query))
            connection.commit()
        print("Table created.")
    except Exception as e:
        print_error_msg(e)
    finally:
        engine.dispose()

def truncate_table(table_name) -> None:
    # SQL statement to truncate a table
    truncate_table_query = f'TRUNCATE TABLE {table_name} RESTART IDENTITY'
    
    try:
        engine = connect_rds()
        with engine.connect() as connection:
            connection.execute(text(truncate_table_query))
            connection.commit()
        print(f"Table {table_name} truncated.")
    except Exception as e:
        print_error_msg(e)
    finally:
        engine.dispose()

def drop_table(table_name) -> None:
    # SQL statement to truncate a table
    drop_table_query = f'DROP TABLE {table_name}'

    try:
        engine = connect_rds()
        with engine.connect() as connection:
            connection.execute(text(drop_table_query))
            connection.commit()
        print(f"Table {table_name} dropped.")
    except Exception as e:
        print_error_msg(e)
    finally:
        engine.dispose()

def store_data_in_rds(insert_query, rows_to_insert):
    try:
        engine = connect_rds()
        with engine.connect() as connection:
            for row in rows_to_insert:
                connection.execute(text(insert_query), row)
            connection.commit()
        print("Data inserted.")
    except Exception as e:
        print_error_msg(e)
    finally:
        engine.dispose()

def run_query(query_string):
    
    try:
        engine = connect_rds()

        # Execute the query
        with engine.connect() as connection:
            result = connection.execute(text(query_string))

            # Fetch the results
            for row in result.fetchall():
                print(row)
    except Exception as e:
        print_error_msg(e)
    finally:
        engine.dispose()   

def create_table_from_df(table_name, df, batch_size=1000, enable_multi_threading=False):
    """
    Create table in RDS from a Pandas dataframe using batch insertions and multi-threading.
    
    Args:
    - table_name (str): The name of the table to create or replace.
    - df (pandas.DataFrame): The DataFrame to write to SQL.
    - batch_size (int): Number of rows per batch to write to the database.
    - enable_multi_threading (bool): True to enable multi-threaded writes, False to use single-threaded.
    """
    try:
        engine = connect_rds()
        with engine.begin() as connection:
            print('Create table from Pandas DataFrame')
            df.to_sql(
                table_name,
                con=connection,
                index=False,
                if_exists='replace',
                chunksize=batch_size,
                method='multi' if enable_multi_threading else None
            )
    except Exception as e:
        print_error_msg(e)
    finally:
        engine.dispose()  # Properly dispose of the connection


def inspect_tables():
    engine = connect_rds()
    inspector = inspect(engine)

    # Get list of table names
    tables = inspector.get_table_names()
    print(sorted(tables))

def save_table_to_csv(table_name, outfile_name):

    engine = connect_rds()

    query = f'SELECT * FROM {table_name}'

    # Load the data into a Pandas DataFrame
    df = pd.read_sql(query, engine)
    df.to_csv(outfile_name)

if __name__ =='__main__':
    inspect_tables()
