import pandas as pd
import requests 
import re
import json

from decouple import config
from sqlalchemy import create_engine
from datetime import datetime
from deepdiff import DeepDiff
from typing import Union, Tuple

from details import main_scraper
from base.db_connection import database_connector


mysql_alchemy_url = str(config("MYSQL_ALCHEMY_URL"))
DB_TABLE_NAME = "precondo"

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


def connect_database_with_sql_alchemy():
     try:
          url = mysql_alchemy_url
          engine = create_engine(url)
          return engine
     
     except Exception as e:
          print(f"Error occured while connecting with pymysql : {e}")


def get_database_data(engine):
     sql_query = "SELECT  id, link, img_src, price, price_range, occupancy, suites, storeys, developer, one_bed_starting_from, two_bed_starting_from, price_per_sqft, avg_price_per_sqft, city_avg_price_per_sqft, development_levies, parking_cost, parking_maintenance, assignment_fee_free, storage_cost, deposit_structure, details, amenities, last_updated, created_at, updated_at, floor_plan, incentives FROM precondo WHERE deleted_at is NULL"
     
     df = pd.read_sql(sql_query, con=engine)
     return df


def fetch_link(i, link : str) -> dict:
     # response = requests.request("GET", link, params=QUERYSTRING, data=PAYLOAD, headers=HEADERS)
     response = requests.get(link)
     
     if response.status_code == 200 and response.content.strip():
          try:
               result_obj = main_scraper(i, link)

               img_src = result_obj.get('img_src',[])
               price = result_obj.get('price')
               price_range = result_obj.get('price_range')
               occupancy = result_obj.get('occupancy')
               occupancy = re.sub(r'[a-zA-Z]','', occupancy)
               suites = result_obj.get('suites')
               storeys =  result_obj.get('storeys')
               developer = result_obj.get('developer')
               one_bed_starting_from = result_obj.get('one_bed_starting_from')
               two_bed_starting_from = result_obj.get('two_bed_starting_from')
               price_per_sqft = result_obj.get('price_per_sqft')
               avg_price_per_sqft = result_obj.get('avg_price_per_sqft')
               city_avg_price_per_sqft = result_obj.get('city_avg_price_per_sqft')
               development_levies = result_obj.get('development_levies')
               parking_cost = result_obj.get('parking_cost')
               parking_maintenance = result_obj.get('parking_maintenance')
               assignment_fee_free = result_obj.get('assignment_fee_free')
               storage_cost = result_obj.get('storage_cost')
               deposit_structure = result_obj.get('deposit_structure')
               details = result_obj.get('details')
               amenities = result_obj.get('amenities',[])
               last_updated = result_obj.get('last_updated')
               floor_plan = result_obj.get('floor_plan',{})
               incentives = result_obj.get('incentives')
               
               status_404 = 0
               
          except Exception as e:
               print(f"Error while scraping data from link in fetch_url --> {link} : {e}")
               img_src = price = price_range = occupancy = suites = storeys = developer = one_bed_starting_from = two_bed_starting_from = price_per_sqft = avg_price_per_sqft = city_avg_price_per_sqft = development_levies = parking_cost = parking_maintenance = assignment_fee_free = storage_cost = deposit_structure = details = amenities = last_updated = floor_plan = incentives = None
               
               status_404 = 1
               
     elif response.status_code == "205":
          img_src = price = price_range = occupancy = suites = storeys = developer = one_bed_starting_from = two_bed_starting_from = price_per_sqft = avg_price_per_sqft = city_avg_price_per_sqft = development_levies = parking_cost = parking_maintenance = assignment_fee_free = storage_cost = deposit_structure = details = amenities = last_updated = floor_plan = incentives = None
               
          status_404 = 1
     
     else:
          img_src = price = price_range = occupancy = suites = storeys = developer = one_bed_starting_from = two_bed_starting_from = price_per_sqft = avg_price_per_sqft = city_avg_price_per_sqft = development_levies = parking_cost = parking_maintenance = assignment_fee_free = storage_cost = deposit_structure = details = amenities = last_updated = floor_plan = incentives = None
               
          status_404 = 0
          
     return {
          'link' : link,
          'img_src' : img_src if img_src else [],
          'price' : price,
          'price_range' : price_range,
          'occupancy' : occupancy,
          'suites' : suites,
          'storeys' : storeys,
          'developer' : developer,
          'one_bed_starting_from' : one_bed_starting_from,
          'two_bed_starting_from' : two_bed_starting_from,
          'price_per_sqft' : price_per_sqft,
          'avg_price_per_sqft' : avg_price_per_sqft,
          'city_avg_price_per_sqft' : city_avg_price_per_sqft,
          'development_levies' : development_levies,
          'parking_cost' : parking_cost,
          'parking_maintenance' : parking_maintenance,
          'assignment_fee_free' : assignment_fee_free,
          'storage_cost' : storage_cost,
          'deposit_structure' : deposit_structure,
          'details' : details,
          'amenities' : amenities if amenities else [],
          'last_updated' : last_updated,
          'floor_plan' : floor_plan or {},
          'incentives' : incentives,
          'status_404' : status_404
          
     }
          

def deleted_not_found_item(result : dict) -> None:
     query_tuple = (datetime.now().strftime("%y-%m-%d %H:%M:%S"), datetime.now().strftime("%y-%m-%d %H:%M:%S"), result['link'])
     sql_query  = f"UPDATE {DB_TABLE_NAME} SET deleted_at = %s, updated_at = %s WHERE link = %s" 
     
     cursor, db_connection = database_connector(autocommit=True)
     cursor.execute(sql_query, query_tuple)
     db_connection.commit()
     print(f"Successfully deleted the data of link : {result['link']}")
     
     
def validation_with_db(db_data: pd.DataFrame, scraped_data: dict) -> Tuple[Union[dict, None], bool]:
     VALUE_CHANGED = False
     IMAGES_CHANGED = False
     changed_extracted_data = {}

     db_row = db_data[db_data["link"] == scraped_data["link"]]

     if not db_row.empty:
          changed_row = {}
          
          for key, scraped_value in scraped_data.items():
               if key in db_row.columns:
                    db_value = db_row[key].iloc[0]
                    db_value = None if db_value in ["", 'nan','null'] else db_value
                    scraped_value = None if scraped_value in ['',0,] else scraped_value

                    # print(f"Processing key: {key}, db_value: {db_value}, scraped_value: {scraped_value}")
                    
                    # Handle lists
                    if key == 'img_src':
                         
                         if isinstance(db_value, str):
                              db_value_list = db_value.split(',') 
                         else:
                              db_value_list = db_value if db_value else []
                              
                         scraped_value_list = scraped_value or []

                         if len(db_value_list) != len(scraped_value_list):
                              print(f"{key} -- {db_value_list} changed_to {scraped_value_list}")
                              IMAGES_CHANGED = True
                              changed_row[key] = scraped_value

                    elif key == "amenities":
                         
                         if isinstance(db_value, str):
                              db_value_list = db_value.split(',') 
                         else:
                              db_value_list = db_value or []
                              
                         scraped_value_list = scraped_value or []

                         if len(db_value_list) != len(scraped_value_list):
                              print(f"{key} -- {db_value_list} changed_to {scraped_value_list}")
                              VALUE_CHANGED = True
                              changed_row[key] = scraped_value

                    # Handle numbers
                    elif key in [
                         'price', 'occupancy', 'suites', 'storeys', 'one_bed_starting_from',
                         'two_bed_starting_from','price_per_sqft', 'avg_price_per_sqft', 'city_avg_price_per_sqft',
                         'parking_cost', 'parking_maintenance', 'storage_cost'
                    ]:
                         if db_value is not None and scraped_value is not None:
                              try:
                                   if float(db_value) != float(scraped_value):
                                        print(f"{key} -- {db_value} changed_to {scraped_value}")
                                        VALUE_CHANGED = True
                                        changed_row[key] = scraped_value
                              except ValueError:
                                   if str(db_value) != str(scraped_value):
                                        print(f"{key} -- {db_value} changed_to {scraped_value}")
                                        VALUE_CHANGED = True
                                        changed_row[key] = scraped_value
                         else:
                              changed_row[key] = scraped_value

                    # Handle dictionaries
                    elif key == "floor_plan":
                         
                         if isinstance(db_value, str):
                              try:
                                   db_value_dict = json.loads(db_value)
                                   # print(db_value_dict)
                                   # print("")
                              except json.JSONDecodeError:
                                   print("Error while changing db_value to json data --> {db_value}")
                                   db_value_dict = db_value or {}
                         else:
                              db_value_dict = db_value or {}
                         scraped_value_dict = scraped_value or {}
                         # print(scraped_value_dict)

                         diff = DeepDiff(db_value_dict, scraped_value_dict, ignore_order=True).to_dict()
                         if diff:
                              print(f"{key} -- {db_value_dict} changed_to {scraped_value_dict}")
                              VALUE_CHANGED = True
                              changed_row[key] = scraped_value
                         
                    # Handle strings
                    else:
                         if str(db_value) != str(scraped_value):
                              print(f"{key} -- {db_value} changed_to {scraped_value}")
                              VALUE_CHANGED = True
                              changed_row[key] = scraped_value

          if VALUE_CHANGED or IMAGES_CHANGED:
               changed_row['id'] = db_row['id']
               changed_row['link'] = scraped_data['link']
               changed_row['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               changed_extracted_data.update(changed_row)

     else:
          print(f"Link not found in database: {scraped_data['link']}")
          VALUE_CHANGED = True
          changed_extracted_data.update(scraped_data)

     if VALUE_CHANGED or IMAGES_CHANGED:
          return changed_extracted_data, IMAGES_CHANGED
     else:
          return None, IMAGES_CHANGED


def update_data(changed_data: dict) -> None:
     cursor, db_connection = database_connector(autocommit=False)
     update_fields = [f'{key} = %s' for key in changed_data.keys() if key not in ['id', 'link']]
     update_query = f"UPDATE {DB_TABLE_NAME} SET {','.join(update_fields)} WHERE link = %s"
     
     update_values = [json.dumps(changed_data[key]) for key in changed_data.keys() if key not in ['id', 'link']]
     update_values.append(changed_data['link'])

     try:
          cursor.execute(update_query, tuple(update_values))
          db_connection.commit()
          print(f"Successfully updated data for the link: {changed_data['link']}")
          print("")
     except Exception as e:
          db_connection.rollback()
          print(f"Error while updating the data in Database for link ---> {changed_data['link']}: {e}")


def link_runner(i, link, db_data):
     try:
          print(i, link)       
          result = fetch_link(i, link)
          
          if result['status_404'] == 1:
               deleted_not_found_item(result)
          else:
               changed_data, IMAGES_CHANGED = validation_with_db(db_data, result)
               
               if changed_data is not None and isinstance(changed_data, dict):
                    update_data(changed_data)
               else:
                    print(f"<--- No Change ---> on link <--- {link} --->")
                    print("")

     except Exception as e:
          print(f"Error occured while gettng data in link_runner from link ----> {link}  : {e}")


def main():
     engine = connect_database_with_sql_alchemy()
     db_data = get_database_data(engine)
     
     links = db_data['link'].tolist()
     # links = ['https://precondo.ca/strata-condos/']
     
     if len(links) > 0:
          for i,link in enumerate(links):
               link_runner(i, link, db_data)
     
     print("Successfully updated All the Data")



if __name__ == "__main__":
     main()