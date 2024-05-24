from sqlalchemy import create_engine, text, inspect
import os
from dotenv import load_dotenv
import pandas as pd

def connect_rds():
    # This function creates a connection to the RDS instance
    # Load environment variables from .env file
    load_dotenv()

    # Database credentials and connection details
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    PORT = '5432'  

    # Database connection URL
    DATABASE_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"

    # Create an engine instance
    engine = create_engine(DATABASE_URL, echo=True)
    return engine

def create_table_if_not_exists(create_table_query):

    engine = connect_rds()  
    try:
        with engine.connect() as connection:
            connection.execute(text(create_table_query))
            connection.commit()
        print("Table truncated.")
    except Exception as e:
        print(f"An error occurred: {e}")

def truncate_table(table_name) -> None:
    # SQL statement to truncate a table
    truncate_table_query = f'TRUNCATE TABLE {table_name} RESTART IDENTITY'
    engine = connect_rds()

    try:
        with engine.connect() as connection:
            connection.execute(text(truncate_table_query))
            connection.commit()
        print("Table truncated.")
    except Exception as e:
        print(f"An error occurred: {e}")

def drop_table(table_name) -> None:
    # SQL statement to truncate a table
    truncate_table_query = f'DROP TABLE {table_name}'
    engine = connect_rds()

    try:
        with engine.connect() as connection:
            connection.execute(text(truncate_table_query))
            connection.commit()
        print("Table dropped.")
    except Exception as e:
        print(f"An error occurred: {e}")

def store_data_in_rds(insert_query, rows_to_insert):
    engine = connect_rds()
    try:
        with engine.connect() as connection:
            for row in rows_to_insert:
                connection.execute(text(insert_query), row)
            connection.commit()
        print("Data inserted.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_query(query_string):
    engine = connect_rds()

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(text(query_string))

        # Fetch the results
        for row in result.fetchall():
            print(row)

def create_table_from_df(table_name, df):
    """
    Create table in RDS from a Pandas dataframe.
    """
    engine = connect_rds()
    df.to_sql(table_name, con=engine, index=False, if_exists='replace')

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
