import os
import sys
import pandas as pd
import numpy as np

# Starting from the current script (insert_to_db.py), get the path to El-salvador directory
current_dir = os.path.dirname(__file__)
el_salvador_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add El-salvador directory to sys.path
sys.path.append(el_salvador_dir)

from base.db_connection import connect_database

def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by replacing NaN values with None.
    None values will be inserted as NULL in MySQL.
    """
    # Replace NaN values with None for all columns
    # df = df.apply(lambda x: None if pd.isna(x) else x)
    df = df.replace({pd.NA: None, np.nan: None})

    return df

def insert_into_table(cursor, table, df):
    """
    Insert DataFrame rows into the specified MySQL table.
    """
    # Prepare placeholders for each column
    placeholders = ', '.join(['%s'] * len(df.columns))
    columns = ', '.join(df.columns)
    
    # Construct the SQL insert query
    insert_query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    
    try:
        # Iterate through each row and insert into the database
        for index, row in df.iterrows():
            # Convert row to tuple and insert using cursor
            cursor.execute(insert_query, tuple(row))
    except Exception as e:
        # Print any errors that occur during insertion
        print(f'Error while inserting into Database : {e}')

def main():
    """
    Main function to execute the process of loading data, cleaning it, 
    and inserting it into the database.
    """
    # Establish database connection and cursor
    db_connections, cursor = connect_database(autocommit=True)
    
    # Table name
    table = 'elsalvador'
    
    # Load data from CSV into DataFrame
    df = pd.read_csv('detail.csv')
    
    # Clean the DataFrame (replace NaNs with None)
    cleaned_df = data_cleaning(df)
    
    # Insert the cleaned data into the database
    insert_into_table(cursor, table, cleaned_df)
    
    print('Data Insertion into Database Completed')

if __name__ == '__main__':
    main()
