import re
import uuid
import pandas as pd
import numpy as np
from datetime import datetime
from base.db_connection import database_connector




def unique_uuid_generator(df):
    existing_uuid = set(df['uuid'])
    while True:
        new_uuid = str(uuid.uuid4())
        if new_uuid not in df['uuid']:
            return new_uuid
    

def data_cleaning(df):
    df.dropna(subset=['title','img_src'], inplace=True)
    df['occupancy'] = df['occupancy'].str.replace(r'[a-zA-Z]','', regex=True)
    df['created_at'] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]
    df = df.replace({pd.NA : None, np.nan : None})
    df.rename(columns={"url":"link","parking_costs":"parking_cost","parking_costs_unit":"parking_cost_unit","parkin_maintenance":"parking_maintenance"}, inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    return df

    
def insert_to_database(df, cursor, t_name):
    columns = ','.join(df.columns)
    placeholders = ','.join(len(df.columns) * ['%s'])

    insert_query = f"INSERT INTO {t_name} ({columns}) VALUES ({placeholders})"

    try:
        for index, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

    except Exception as e:
        print(f"Error while inserting data into database : {e}")
    # insert into table (columns) values() 


def main():
    df = pd.read_csv('details.csv')
    cursor, db_connection = database_connector(autocommit=True)
    t_name = 'precondo'

    cleaned_df = data_cleaning(df)
    insert_to_database(cleaned_df, cursor, t_name)
    print("Successfully inserted data into database")



if __name__ == "__main__":
    main()


