import pandas as pd
import os 
import sys

# Starting from the current script (insert_to_db.py), get the path to El-salvador directory
current_dir = os.path.dirname(__file__)
el_salvador_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add El-salvador directory to sys.path
sys.path.append(el_salvador_dir)

from base.db_connection import connect_database

def data_cleaning(df: pd.DataFrame)-> pd.DataFrame:
     df['deleted_at'] = None
     
     df = df.where(pd.notna(df), None)
     
     return df


def insert_into_table(cursor, table, df):
     placeholders = ', '.join(['%s'] * len(df.columns))
     columns = ', '.join(df.columns)
     insert_query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
     
     try:
          # iteration through each row
          for index, row in df.iterrows():
               cursor.execute(insert_query, tuple(row))
               
     except Exception as e:
          print(f'Error while inserting into Database : {e}')
          
          
def main():
     db_connections , cursor = connect_database(autocommit=True)
     
     table = 'elsalvador'
     
     df = pd.read_csv('detail.csv')
     
     cleaned_df = data_cleaning(df)
     
     insert_into_table(cursor, table, cleaned_df)
     
     print('Data Insetion into Database Completed')
     

if __name__  ==  '__main__':
     main()
     
     
     
     
     
     