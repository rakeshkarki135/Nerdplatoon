import datetime
import pandas as pd

from base.db_connection import connect_database

def data_cleaning(df):
     # Remove commas in the 'exterior' column and convert to float
     df['Exterior'] = df['Exterior'].astype(float)
     # Drop rows with missing critical columns 'title' or 'img_src'
     df.dropna(subset=['title', 'img_src'], inplace=True)
     # Replace NaN values with None
     df = df.map(lambda x: None if pd.isna(x) else x)
     df = df.rename(columns={'Exterior':'exterior','Web Id':'web_id','MLS ID':'mls_id','Bedrooms':'bedrooms','Full Baths':'full_baths','Property Type':'property_type','Interior':'interior','Partial Baths':'partial_baths','Property Details':'property_details'})
     
     return df

# insert data into database
def insert_to_database(cursor, table_name, df):
     parameters = ','.join(['%s'] * len(df.columns))
     columns = ','.join(df.columns)
     insert_query = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({parameters})"
     try:
          for index, row in df.iterrows():
               # Replace NaN/None with NULL explicitly if required
               row = tuple(None if pd.isna(val) else val for val in row)
               cursor.execute(insert_query, row)
     except Exception as e:
          print(f'Error while inserting data into database : {e}')


def main():
     db_connection, cursor = connect_database(autocommit=True)
     
     df = pd.read_csv('details.csv')
     new_df = data_cleaning(df)
     
     table_name = 'bahamas'
     insert_to_database(cursor, table_name, new_df)
     
     print("Data Inserted into the Database")

if __name__ == '__main__':
     main()
