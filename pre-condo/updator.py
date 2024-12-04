import pandas as pd
import requests 

from decouple import config
from sqlalchemy import create_engine
from datetime import datetime
from deepdiff import DeepDiff
from typing import Union, Tuple

from details import url_handler
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
     sql_query = "SELECT  link, img_src, price, price_range, occupancy, suites, storeys, developer, one_bed_starting_from, two_bed_starting_from, price_per_sqft, avg_price_per_sqft, city_avg_price_per_sqft, development_levies, parking_cost, parking_maintenance, assignment_fee_free, storage_cost, deposit_structure, details, amenities, last_updated, created_at, updated_at, deleted_at, floor_plan, incentives FROM precondo WHERE deleted_at is NULL"
     
     df = pd.read_sql(sql_query, con=engine)
     return df


def fetch_link(link : str) -> dict:
     response = requests.request("GET", link, params=QUERYSTRING, data=PAYLOAD, headers=HEADERS)
     
     if response.status_code == 200 and response.content.strip():
          try:
               result_df = url_handler()
               
               def get_value(col):
                    return result_df[col].iloc[0] if (col in result_df.columns and pd.notna(result_df[col].iloc[0])) else None
               
               img_src = get_value('img_src')
               price = get_value('price')
               price_range = get_value('price_range')
               occupancy = get_value('occupancy')
               suites = get_value('suites')
               storeys =  get_value('storeys')
               developer = get_value('developer')
               one_bed_starting_from = get_value('one_bed_starting_from')
               two_bed_starting_from = get_value('two_bed_starting_from')
               price_per_sqft = get_value('price_per_sqft')
               avg_price_per_sqft = get_value('avg_price_per_sqft')
               city_avg_price_per_sqft = get_value('city_avg_price_per_sqft')
               development_levies = get_value('development_levies')
               parking_cost = get_value('parking_cost')
               parking_maintenance = get_value('parking_maintenance')
               assignment_fee_free = get_value('assignment_fee_free')
               storage_cost = get_value('storage_cost')
               deposit_structure = get_value('deposit_structure')
               details = get_value('details')
               amenities = get_value('amenities')
               last_updated = get_value('last_updated')
               floor_plan = get_value('floor_plan')
               incentives = get_value('incentives')
               
               status_404 = 0
               
          except Exception as e:
               print("Error while getting scraping data in link --> {link} : {e}")
               img_src = price = price_range = occupancy = suites = storeys = developer = one_bed_starting_from = two_bed_starting_from = price_per_sqft = avg_price_per_sqft = city_avg_price_per_sqft = development_levies = parking_cost = parking_maintenance = assignment_fee_free = storage_cost = deposit_structure = details = amenities = last_updated = floor_plan = incentives = 1
               
               status_404 = 1
               
     elif response.status_code == "205":
          img_src = price = price_range = occupancy = suites = storeys = developer = one_bed_starting_from = two_bed_starting_from = price_per_sqft = avg_price_per_sqft = city_avg_price_per_sqft = development_levies = parking_cost = parking_maintenance = assignment_fee_free = storage_cost = deposit_structure = details = amenities = last_updated = floor_plan = incentives = 1
               
          status_404 = 1
     
     else:
          img_src = price = price_range = occupancy = suites = storeys = developer = one_bed_starting_from = two_bed_starting_from = price_per_sqft = avg_price_per_sqft = city_avg_price_per_sqft = development_levies = parking_cost = parking_maintenance = assignment_fee_free = storage_cost = deposit_structure = details = amenities = last_updated = floor_plan = incentives = 1
               
          status_404 = 0
          
     return {
          'link' : link,
          'img_src' : img_src,
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
          'amenities' : amenities,
          'last_updated' : last_updated,
          'floor_plan' : floor_plan,
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
     
     
def validation_with_db(db_data : pd.DataFrame, scraped_data : dict) -> Tuple[Union[dict , None], bool]:
     VALUE_CHANGED = False
     IMAGES_CHANGED = False
     changed_extracted_data = {}

     db_row = [db_data["link"] == scraped_data["link"]]

     if not db_row.empty:
          changed_row = {}
          db_row = db_row.iloc[0]

          for  key, scraped_value in scraped_data.items():
               if key in db_row.index:
                    db_value = db_row[key]

                    db_value = None if db_value == '' else db_value

                    # for lists
                    if key in ['img_src']:
                         # db_value_list = db_value.split(",") if db_value else []
                         # scraped_value_list = scraped_value.split(",") if scraped_value else []
                        
                         if len(db_value) != len(scraped_value):
                             IMAGES_CHANGED = True
                             changed_row[key] = scraped_value      

                    elif key == "amenities":
                         if len(db_value) != len(scraped_value):
                              VALUE_CHANGED = True
                              changed_row[key] = scraped_value

                    # for interger or float value
                    elif key in ['price','occupancy','suites','storeys','one_bed_starting_from','one_bed_starting_from',
                                 'price_per_sqft','avg_price_per_sqft','city_avg_price_per_sqft','parking_cost','parkin_maintenance','storage_cost']:

                         if db_value is not None and scraped_value is not None:
                              try:
                                   if float(len(db_value)) != float(len(scraped_value)):
                                        VALUE_CHANGED = True
                                        changed_row[key] = scraped_value
                         
                              except ValueError:
                                   if str(db_value) != str(scraped_value):
                                        VALUE_CHANGED = True
                                        changed_row[key] = scraped_value
                         else:
                              changed_row[key] = scraped_value

                    # for dictionaries
                    elif key == "floor_plan":
                         diff = DeepDiff(db_value, scraped_value, ignore_order=True).to_dict()
                         if diff:
                              VALUE_CHANGED = True
                              changed_row[key] = scraped_value
                    

                    # maily for strings
                    else:
                         if str(db_value) != str(scraped_value):
                              VALUE_CHANGED = True
                              changed_row[key] = scraped_value

          if VALUE_CHANGED or IMAGES_CHANGED:
               changed_row['id'] = db_row['id'].iloc[0]
               changed_row['link'] = scraped_data['link']
               changed_row['updated_at'] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
               changed_extracted_data.update(changed_row)

     else:
          print(f"Link not found in database : {scraped_data['link']}")    
          VALUE_CHANGED = True
          changed_extracted_data.update(scraped_data)


     if IMAGES_CHANGED or VALUE_CHANGED:
          return IMAGES_CHANGED, changed_extracted_data
     else:
          return IMAGES_CHANGED, None
     

def update_data(changed_data : dict) -> None:
     cursor, db_connection = database_connector(autocommit=False)
     update_fields = [f'{key} = %s' for key in changed_data.keys() if key not in ['id','link']]
     update_query = f"UPDATE {DB_TABLE_NAME} SET ({','.join(update_fields)}) WHERE link = %s"
     update_values = [str(changed_data[key]) for key,value in changed_data.items() if key not in ['id','link']]
     update_values.append(changed_data['link'])

     try:
          cursor.execute(update_query, tuple(update_values))
          db_connection.commit()
          print(f"Successfully updated data for the link : {changed_data['link']}")

     except Exception as e:
          db_connection.rollback()
          print(f"Error while updating the data in Database for link ---> {changed_data['link']}: {e}")


def url_handler(i, link, db_data):
     try:
          print(i, link)
                    
          result = fetch_link(link)
          
          if result['status_404']:
               deleted_not_found_item(result)
          else:
               changed_data, IMAGES_CHANGED = validation_with_db(db_data, result)

               if changed_data is not None and isinstance(changed_data, dict):
                    update_data(changed_data)
               else:
                    print("<--- No Change ---> on link <--- {link} --->")

     except Exception as e:
          print(f"Error occured while gettng data from link ----> {link}  : {e}")


def main():
     engine = connect_database_with_sql_alchemy()
     db_data = get_database_data(engine)

     print(db_data)
     
     links = db_data['link'].tolist()
     
     if len(links) > 0:
          for i,link in enumerate(links):
               url_handler(i, link, db_data)
               
     
     print("All the data updated Successfully")



if __name__ == "__main__":
     main()