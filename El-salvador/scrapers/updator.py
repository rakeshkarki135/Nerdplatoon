import os 
import sys   
import pandas as pd
import requests
import json

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from sqlalchemy import create_engine
from main import detailScraper

current_dir = os.path.dirname(__file__)
elsalvador_dir = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(elsalvador_dir)
from base.db_connection import connect_database

QUERYSTRING = {"ajaxcall":"true","ajaxtarget":"privatenotes,listingmeta,customlistinginfo_attributiontext,listingdetailsmap,routeplanner,listingcommunityinfo,metainformation,listingmeta_bottom,listingmedia,listingpropertydescription,listingtabtitles,listingtools_save_bottom,customlistinginfo_commentsshort,listingtools,listingtools_mobile,listinginfo,listingmarkettrendsmodule,localguidelistingdetailspage,listingdrivetime,listingphotos,listingdetails","cms_current_mri":"119274"}
PAYLOAD = ""
HEADERS = {
     "accept": "application/xml, text/xml, */*; q=0.01",
     "accept-language": "en-US,en;q=0.9",
     "cache-control": "no-cache",
     "pragma": "no-cache",
     "priority": "u=1, i",
     "sec-ch-ua-mobile": "?0",
     "sec-ch-ua-platform": "Windows",
     "sec-fetch-dest": "empty",
     "sec-fetch-mode": "cors",
     "sec-fetch-site": "same-origin",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
     "x-requested-with": "XMLHttpRequest"
}
DB_TABLE_NAME = 'elsalvador'


def driver_initialization():
     options = webdriver.ChromeOptions()
     # Configure Chrome options
     options.add_argument("--headless")  # Run in headless mode
     options.add_argument("--disable-gpu")  # Disable GPU acceleration
     options.add_argument("--disable-webgl")
     options.add_argument("--disable-software-rasterizer")
     options.add_argument("--log-level=3")  # Suppress logs
     service = webdriver.ChromeService()
     driver = webdriver.Chrome(service=service, options=options)
     return driver
     

def connect_database_with_sqlalchemy():
     try:
          url = 'mysql+pymysql://root:@localhost:3306/nerdpractice'
          engine = create_engine(url)
          return engine
     except Exception as e:
          print(f'Error while connecting database with sqlAlchemy : {e}')


def get_database_data(engine):
     query = "SELECT id, uuid, title, link, location, country, price, code_number, property_type, type, bedrooms, full_baths, half_baths, description, construction_area, area_square_vara, levels, parking, privacy, img_src, previous_price, phone, price_unit FROM elsalvador WHERE deleted_at is NULL"
     
     df = pd.read_sql(query, con=engine)
     return df


def fetch_link(i, driver, link : str) -> dict:
     response = requests.request("GET", link, data=PAYLOAD, headers=HEADERS, params=QUERYSTRING)
     df = pd.DataFrame(columns=['uuid', 'price', 'property_type', 'type', 'bedrooms', 'full_baths', 'half_baths', 'description', 'construction_area', 'area_square_vara', 'levels', 'parking', 'privacy', 'img_src'])
     
     if response.status_code == 200 and response.content.strip():
          try:
               result_df = detailScraper(i, df, link, driver)
               #function to convert nan value to None
               def get_value(col):
                    return result_df[col].iloc[0] if (col in result_df.columns and pd.notna(result_df[col].iloc[0])) else None
               
               price = get_value('price')
               property_type = get_value('property_type')
               type = get_value('type')
               bedrooms = get_value('bedrooms')
               full_baths = get_value('full_baths')
               half_baths = get_value('half_baths')
               description = get_value('description')
               construction_area = get_value('construction_area')
               area_square_vara = get_value('area_square_vara')
               levels = get_value('levels')
               parking = get_value('parking')
               privacy = get_value('privacy')
               img_src = get_value('img_src')
                    
               status_404 = 0
          
          except TimeoutException as e:
               print(f'TimeOutException : Conetnt not found for link : {link}')
               price = property_type = type = bedrooms = full_baths = half_baths = description = construction_area = area_square_vara = levels = parking = privacy = img_src = None
               status_404 = 1
               
               
     elif response.status_code == 205:
          price = property_type = type = bedrooms = full_baths = half_baths = description = construction_area = area_square_vara = levels = parking = privacy = img_src = None
          
          status_404 = 1
     
     else:
          price = property_type = type = bedrooms = full_baths = half_baths = description = construction_area = area_square_vara = levels = parking = privacy = img_src = None
          
          status_404 = 0
          
     return {
          'price' : price,
          'property_type' : property_type, 
          'type': type, 
          'link' : link,
          'bedrooms' : bedrooms, 
          'full_baths' : full_baths, 
          'half_baths' : half_baths, 
          'description' : description, 
          'construction_area' : construction_area, 
          'area_square_vara' : area_square_vara, 
          'levels' : levels, 
          'parking' : parking, 
          'privacy' : privacy, 
          'img_src' : img_src, 
          'status_404' : status_404
     }
     
def get_link_id_from_db(link : str) -> int:
     engine = connect_database_with_sqlalchemy()
     query = f'SELECT id, link from {DB_TABLE_NAME} WHERE link = %s'
     df = pd.read_sql(query, con=engine, params=(link,))
     return df['id'].iloc[0]
     
     
def delete_not_found_item(result : dict) -> None:
     query_tuple = (datetime.now().strftime("%y-%m-%d %H:%M:%S"), datetime.now().strftime("%y-%m-%d %H:%M:%S"), result['link'])
     query = f"UPDATE {DB_TABLE_NAME} SET deleted_at = %s, updated_at = %s WHERE link = %s"
     db_connection, cursor = connect_database(autocommit=True)
     cursor.execute(query, query_tuple)
     db_connection.commit()
     id_of_link_from_db = get_link_id_from_db(result['link'])
     print(f"Successfully deleted the data of link : {result['link']} with id : {id_of_link_from_db}")

def validation_with_db(db_data: pd.DataFrame, extracted_data: dict) -> tuple[dict | None, bool]:
     VALUE_CHANGED = False
     IMAGES_CHANGED = False
     changed_extracted_data = {}

     # Find the row in the database that matches the extracted data's link
     db_row = db_data[db_data['link'] == extracted_data['link']]

     # Check if the row was found
     if not db_row.empty:
          changed_row = {}
          db_row = db_row.iloc[0]  # Get the first matching row as a Series

          for key, extracted_value in extracted_data.items():
               if key in db_row.index:  # Check if the key exists in db_row columns
                    db_value = db_row[key]

                    # Convert empty strings to None for consistency
                    db_value = None if db_value == '' else db_value

                    # Special case for images (comma-separated string comparison)
                    if key == 'img_src':
                         db_value_list = db_value.split(',') if db_value else []
                         extracted_value_list = extracted_value.split(',') if extracted_value else []

                         if len(extracted_value_list) != len(db_value_list):
                              IMAGES_CHANGED = True
                              changed_row[key] = extracted_value

                    # Numerical fields comparison
                    elif key in ['price', 'bedrooms', 'full_baths', 'half_baths', 
                              'construction_area', 'area_square_vara', 'levels', 'parking']:
                         if extracted_value is not None and db_value is not None:
                              try:
                                   if float(extracted_value) != float(db_value):
                                        VALUE_CHANGED = True
                                        changed_row[key] = extracted_value
                              except ValueError:
                                   if str(extracted_value) != str(db_value):
                                        VALUE_CHANGED = True
                                        changed_row[key] = extracted_value
                         else:
                              if extracted_value != db_value:
                                   VALUE_CHANGED = True
                                   changed_row[key] = extracted_value

                    # Generic comparison for other fields
                    else:
                         if str(extracted_value) != str(db_value):
                              VALUE_CHANGED = True
                              changed_row[key] = extracted_value

          # If any value has changed, update the result dictionary
          if VALUE_CHANGED or IMAGES_CHANGED:
               changed_row['id'] = db_row['id']
               changed_row['link'] = extracted_data['link']
               changed_row['updated_at'] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
               changed_extracted_data.update(changed_row)

     # If the link is not found in the database
     else:
          print(f"Link not found in database: {extracted_data['link']}")
          VALUE_CHANGED = True
          changed_extracted_data.update(extracted_data)

     # Return the changed data if any changes were detected
     if VALUE_CHANGED or IMAGES_CHANGED:
          return changed_extracted_data, IMAGES_CHANGED
     return None, IMAGES_CHANGED

                              
def update_data(changed_data : dict) -> None:
     db_connection, cursor = connect_database(autocommit=True)
     update_fields = [f"{key} = %s" for key in changed_data.keys() if key not in ['id', 'link']]
     update_query = f"UPDATE {DB_TABLE_NAME} SET {', '.join(update_fields)} WHERE link = %s" 
     # update_values = [changed_data[key] for key in changed_data.keys() if key not in ['id', 'link']]
     update_values = [
          json.dumps(changed_data[key]) if isinstance(changed_data[key], dict) else changed_data[key] for key in changed_data.keys() if key not in ['id','link']
     ]
     
     update_values.append(changed_data['link'])
     
     try:
          db_connection.ping(reconnect=True)
          cursor.execute(update_query, tuple(update_values))
          db_connection.commit()
          print(f"Successfully updated data for link : {changed_data['link']}")
          
     except Exception as e:
          db_connection.rollback()
          print(f'Error while inserting  Data : {e}')


def main():
     engine = connect_database_with_sqlalchemy()
     db_data = get_database_data(engine)
     
     driver = driver_initialization()
     links = db_data['link'].tolist()
     
     if len(links) > 0:
          for i,link in enumerate(links):
               print(i, link)
               result = fetch_link(i, driver, link)
               
               if result['status_404'] == 1:
                    delete_not_found_item(result)
               else:
                    changed_data, IMAGES_CHANGED = validation_with_db(db_data, result)
                    if changed_data is not None and isinstance(changed_data, dict):
                         update_data(changed_data)
                    else:
                         print('No Change')
     driver.quit()


if __name__ == '__main__':
     main()