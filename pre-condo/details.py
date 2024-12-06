import re
import uuid
import requests
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup



def soup_creator(url):
     try:
          cookies = {'authenticated' : '1'}
          response = requests.get(url, cookies=cookies)
          # print(response.status_code)
          html_content = response.content
          soup = BeautifulSoup(html_content, 'lxml')
          main_container = soup.find('div', class_ = 'container my-4')          
          return main_container
     
     except Exception as e:
          print(f"Error while getting main container : {e}")
          return None


def image(soup):
     try:

          img_container = soup.find('div', class_ = 'image-gallery grid-5')
          
          img_src = []
          if img_container:
               img_elements = img_container.find_all('a', class_ = 'popup-image')
               
               if img_elements is not None:
                    for item in img_elements:
                         img = item.get('href')
                         img_src.append(img)
                    # print(img_src)
          else:
               img_src = None

          return img_src
     
     except Exception as e:
          print(f"Error while getting images : {e}")
          
          
def title_and_location(soup):
     try:
          info_container = soup.find('div', class_ = 'property-title')
          
          if info_container:
               # for Title
               title_element = info_container.find('h1')
               title = title_element.text.strip() if title_element else None
               
               # for location
               location_element = info_container.find('p', class_ = 'address-img fs-6')
               location = location_element.text.strip() if location_element else None

               # for price
               price_element = info_container.find('span', class_ = 'fs-1')
               # price = ''.join(re.findall(r'\d+', price_element.text.strip())) if price_element else None
               if price_element:
                    price = price_element.text.strip()
                    if 'From' in price:
                         price = price.replace('From', '').replace('to', '-')
                    else:
                         price = ''.join(re.findall(r'\d+', price))
                         
          return title, location, price
               
     except Exception as e:
          print(f"Error while getting Title and Location : {e}")


def last_updated(soup):
     try:
          last_updated_element = soup.find('p', class_ = "fst-italic")
          if last_updated_element:
               last_updated_date = last_updated_element.text.strip().replace('Last Updated:', '')
               # print(last_updated_date)
          else:
               print("last updated element is not found")
          
          return last_updated_date
     
     except Exception as e:
          print(f"Error while getting last updated date : {e}")


def remove_attributes(element):
     for tag in element.find_all(True):
          tag.attrs = {}
     return element
     
     
def details(soup):
     try:
          details_container = soup.find('div', class_ = 'description__box')
     
          if details_container:
               cleaned_details = remove_attributes(details_container)
               details = cleaned_details.decode_contents()  
               # print(details)  
               
          return details
     except Exception as e:
          print(f"Error while getting details : {e}")



def amenity(soup):
     try:
          amen_container = soup.find("div", class_ = "amenities-div")
          amenities_list = []
          
          if amen_container:
               amen_boxes = amen_container.find_all("div", class_ = "amenity-column")
               # print(len(amen_boxes))
               for box in amen_boxes:
                    amenities_elements = box.find_all("div", class_ = "d-flex")
                    
                    for element in amenities_elements:
                         amenities = element.text.strip() if element else None
                         amenities_list.append(amenities)
          else:
               amenities_list = None
               
          # print(len(amenities_list))
          return amenities_list
     except Exception as e:
          print(f"Error occured while getting Amenities : {e}")


def Overview(soup):
     try:
          overview_con = soup.find('div', class_ = 'overview')

          if not overview_con:
               print("Overview Container is not Found")
               return {}
          
          boxes = overview_con.find_all('div', class_ = 'overview-item')
          overview_obj = {} 

          for box in boxes:
               data_element = box.find('span')
               
               if data_element:
                    values = data_element.text.replace(':','').replace(',', '').split()
                    
                    if len(values) >= 2:
                         key = ''.join(values[0].lower())
                         value = ' '.join(values[1:])
                         overview_obj[key] = None if value == "N/A" else value
               
          # print(overview_obj)
          return overview_obj
          
     except Exception as e:
          print(f"Error whle getting overview details : {e}")
     
# def price_and_incentives(soup):
#      try:
#           table_container = soup.find('div', class_='pricing-fees')
#           if not table_container:
#                return {}

#           table = table_container.find('table', class_='table')
#           if not table:
#                return {}

#           table_rows = table.find_all('tr')
#           if not table_rows:
#                return {}

#           price_incentive = {}

#           # Keys that need price/unit splitting
#           price_keys = [
#                '1_bed_starting_from', '2_bed_starting_from', 'price_per_sqft',
#                'avg_price_per_sqft', 'city_avg_price_per_sqft', 'parking_cost', 
#                'parking_maintenance', 'storage_cost'
#           ]

#           # Keys to directly add
#           direct_keys = ['development_levies', 'incentives', 'deposit_structure', 'price_range']

#           for row in table_rows:
#                columns = row.find_all('td')
#                if len(columns) > 1:  # Ensure at least two columns exist
#                     key = '_'.join(columns[0].text.lower().strip().split())
#                     value = columns[1].text.strip().replace(',', '')
#                     value = None if value == 'Register Now' or value == 'N/A' else value
                    
#                if value is not None:
#                     # Check for keys requiring price and unit splitting
#                     if key in price_keys:
#                          if key in ['1_bed_starting_from', '2_bed_starting_from']:
#                          # Split on '$' to extract the price
#                               sp_value = value.split('$')
#                               if len(sp_value) > 1:
#                                    price_incentive[key] = sp_value[1].replace("'","").replace("s","")
#                                    price_incentive[f"{key}_unit"] = '$'
#                               else:
#                                    price_incentive[key] = value  # Fallback if '$' is missing
#                          else:
#                               split_value = value.split()
#                               if len(split_value) > 1:  # Ensure split is valid
#                                    price = split_value[1]
#                                    unit = split_value[0]
#                                    price_incentive[key] = price
#                                    price_incentive[f"{key}_unit"] = unit
#                               else:
#                                    price_incentive[key] = value  # Fallback if split fails

#                     # Direct addition for specific keys
#                     elif key in direct_keys:
#                          price_incentive[key] = value

#                     # Default case for other keys
#                     else:
#                          price_incentive[key] = value
#                else:
#                     price_incentive[key] = None

#           return price_incentive

#      except Exception as e:
#           print(f"Error while getting the prices and incentives: {e}")
#           return {}

def extract_number(value):
     clean_value = re.sub(r'[\,]', '', value)  
     match = re.search(r'\d+(\.\d+)?', clean_value)  # Search for digits (including decimals)
     return match.group() if match else None

def extract_currency_symbol(value):
     currencies = {"$": "$", "£": "£", "€": "€"}
     for symbol in currencies:
          if symbol in value:
               return symbol
     return None

def price_and_incentives(soup):
     try:
          pricing_incentive = {}
          pricing_incentive_container = soup.find('div', class_='pricing-fees')
          pricing_incentive_table = pricing_incentive_container.find('table')
          pricing_incentive_tablebody = pricing_incentive_table.find('tbody')
          
          for row in pricing_incentive_tablebody.find_all('tr'):
               cells = row.find_all('td')  # Get all <td> elements in the row
               if len(cells) >= 2:  
                    key = cells[0].get_text(strip=True)  
                    value = cells[1].get_text(strip=True)  
                    currency_symbol = extract_currency_symbol(value)

                    if key == 'Price Range':
                         pricing_incentive["price_range"] = None if value == "N/A" else value
                    elif key == '1 Bed Starting From':
                         pricing_incentive["one_bed_starting_from"] = None if value == "Register Now" else extract_number(value)
                         pricing_incentive["one_bed_starting_from_unit"] = None if value is None or value == "Register Now" else currency_symbol
                    elif key == '2 Bed Starting From':
                         pricing_incentive["two_bed_starting_from"] = None if value == "Register Now" else extract_number(value)
                         pricing_incentive["two_bed_starting_from_unit"] = None if value is None or value == "Register Now" else currency_symbol
                    elif key == 'Price Per Sqft':
                         pricing_incentive["price_per_sqft"] = None if value == "N/A" else extract_number(value)
                         pricing_incentive["price_per_sqft_unit"] = None if value == "N/A" else currency_symbol
                    elif key == 'City Avg Price Per Sqft':
                         pricing_incentive["city_avg_price_per_sqft"] = None if value == "N/A" else extract_number(value)
                         pricing_incentive["city_avg_price_per_sqft_unit"] = None if value is None or value == "N/A" else currency_symbol
                    elif key == 'Development Levies':
                         pricing_incentive["development_levies"] = None if value == "N/A" else value
                    elif key == 'Parking Cost':
                         pricing_incentive["parking_cost"] = None if value == "N/A" else extract_number(value)
                         pricing_incentive["parking_cost_unit"] = None if value == "N/A" else currency_symbol
                    elif key == 'Parking Maintenance':
                         pricing_incentive["parking_maintenance"] = None if value == "N/A" else extract_number(value)
                         pricing_incentive["parking_maintenance_unit"] = None if value == "N/A" else currency_symbol
                    elif key == 'Assignment Fee Free':
                         pricing_incentive["assignment_fee_free"] = None if value == "N/A" else value
                    elif key == 'Storage Cost':
                         pricing_incentive["storage_cost"] = None if value == "N/A" else extract_number(value)
                         pricing_incentive["storage_cost_unit"] = None if value == "N/A" else currency_symbol
                    elif key == 'Deposit Structure':
                         pricing_incentive["deposit_structure"] = None if value == "N/A" else value
                    elif key == 'Avg Price Per Sqft':
                         pricing_incentive["avg_price_per_sqft"] = None if value is None else extract_number(value)
                         pricing_incentive["avg_price_per_sqft_unit"] = currency_symbol if value is not None else None
                    elif key == 'Incentives':
                         pricing_incentive['incentives'] = None if value in [None, 'N/A']  else value

          return pricing_incentive

     except Exception as e:
          print(f"Error while getting incentive: {e}")
     
def floor_plan(soup):
     try:
          floor_pln = {}
          floor_pln_container = soup.find("div", id = "floorplans")

          if floor_pln_container:
               # for 1_bed
               floor_pln_boxes = floor_pln_container.find_all("div", class_ = "tab-pane")
               floor_pln_keys = floor_pln_container.find_all('li')
               
               floor_pln_items_obj = {}
               for box, key in zip(floor_pln_boxes, floor_pln_keys):
                    floor_pln_items = box.find_all("div", class_ = "tab-pane-item")
                    floor_pln_key = key.text.strip()
                    # print(len(floor_pln_items))
                    
                    floor_pln_list = []
                    for item in floor_pln_items:
                         floor_plan_details = {}
                         # for img_url
                         img_container = item.find("div", class_ = "col-item col-item-photo")
                         if img_container:
                              img_element = img_container.find("a")
                              if img_element:
                                   img_url = img_element.get("href")
                                   # print(img_url)
                                   floor_plan_details['floorplan'] = img_url
                              
                         # for title   
                         title_element = item.find("div", class_ = "col-item col-item-plan")
                         if title_element:
                              title = title_element.text.strip()
                              # print(title)
                              floor_plan_details['title'] = title
                         
                         # for bed and bath
                         bed_and_bath_element = item.find("div", class_ = "col-item col-item-bed")
                         if bed_and_bath_element:
                              bed_and_bath = bed_and_bath_element.text.strip().split("\n")
                              bed = bed_and_bath[0].split()[0] if len(bed_and_bath) > 0 else None
                              bath = bed_and_bath[1].split()[0] if len(bed_and_bath) > 1 else None
                              
                              # print(bed, bath)
                              floor_plan_details['bedrooms'] = bed 
                              floor_plan_details['bathrooms'] = bath
                         
                         # for area_sqft
                         area_element = item.find("div", class_ = "col-item col-item-sq-ft")
                         if area_element:
                              area_sqft = area_element.text.strip().split()[0]
                              # print(area_sqft)
                              floor_plan_details['area_sqft'] = area_sqft
                              
                         # for price
                         price_container = item.find("div", class_ = "col-item col-item-price is-bold")
                         if price_container:
                              if price_container:
                                   # for price unit
                                   price_unit = price_container.text.strip().split("$")[0] + "$"
                                   # print(price_unit)
                                   floor_plan_details['price_unit'] = price_unit
                              
                              # for price 
                              price_element = price_container.find("span", class_ = "fp-price") 
                              if price_element:
                                   price = price_element.text.strip().replace(',','')
                                   # print(price)
                                   floor_plan_details['price'] = price
                              
                              # for price_sqft
                              price_sqft_element = price_container.find("span", class_ = "fp-price-per-sqft")
                              if price_sqft_element:
                                   price_sqft = price_sqft_element.text.strip()
                                   price_sqft = ''.join(re.findall(r'\d+', price_sqft))
                                   # print(price_sqft)
                                   floor_plan_details['price_sqft'] = price_sqft
                              
                         floor_pln_list.append(floor_plan_details)  
                    
                    floor_pln_items_obj[floor_pln_key.lower()] =  floor_pln_list

               floor_pln['floor_plan'] = floor_pln_items_obj
          return floor_pln
          
     except Exception as e:
          print(f"Error while getting the floor plans : {e}")
     

def functions_handler(soup, *functions):
     results = []
     for func in functions:
          results.append(func(soup))
     
     return results

def main_scraper(i, url):
     try:
          soup = soup_creator(url)

          # Initialize data from functions
          img_src, title_location, overview, price_and_incentive, description, amenities, floor_pln, last_update = \
               functions_handler(soup, image, title_and_location, Overview, price_and_incentives, details, amenity, floor_plan, last_updated)

          # Handle None values and flatten data
          row = {
               'url': url,
               'img_src': img_src if img_src else [],
               'title': title_location[0] if title_location else None,
               'location': title_location[1] if title_location else None,
               'price': title_location[2] if (title_location and len(title_location[2].split()) == 1) else None,
               'price_range': title_location[2] if (title_location and len(title_location[2].split()) > 1) else None,
               **(overview if overview else {}),  # Include all expected keys
               **(price_and_incentive if price_and_incentive else {}),
               'details': description,
               'amenities': amenities if amenities else [],
               'floor_plan' : floor_pln if floor_pln else {},  # Standardize keys
               'last_updated': last_update,
               'created_at': datetime.now().strftime("%y-%m-%d %H:%M:%S"),
               'updated_at': None,
               'deleted_at': None
          }

          return row

     except Exception as e:
          print(f"Error occurred while getting details in main_scraper: {e}")
          return {}

          
def url_extractor():
     urls_df = pd.read_csv('api_urls.csv')
     urls = urls_df['link'].tolist()
     data = []
     
     for i,url in enumerate(urls):
          print(i + 1, url)
          row = main_scraper(i, url)
          data.append(row)
          
     df = pd.DataFrame(data)
     return df
     
def main():
     df = url_extractor()
     df['occupancy'] = df['occupancy'].str.replace(r'[a-zA-Z]','', regex=True)
     df.to_csv('details.csv', index=False)
     
     print("Scraping completed")
     
     
if __name__ == '__main__':
     main()


