import re
import requests
import pandas as pd
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
               price = price_element.text.strip() if price_element else None
               
     
          return title, location, price
               
     except Exception as e:
          print(f"Error while getting Title and Location : {e}")

def Overview(soup):
     try:
          overview_con = soup.find('div', class_ = 'overview')
          boxes = overview_con.find_all('div', class_ = 'overview-item')
          overview_obj = {} 
          for box in boxes:
               data_element = box.find('span')
               
               if data_element:
                    values = data_element.text.split()
                    key = values[0].lower()
                    value = values[1].replace(',','')
                    
                    
                    overview_obj[key] = value
                    
          # print(overview_obj)
          return overview_obj
          
     except Exception as e:
          print(f"Error whle getting overview details : {e}")
     

def price_and_incentives(soup):
     try:
          table_container = soup.find('div', class_ = 'pricing-fees')
          if table_container:
               table = table_container.find('table', class_ = 'table')
               table_rows = table.find_all('tr')
               # print(len(table_rows))
               
               price_incentive = {}
               for row in table_rows:
                    columns = row.find_all('td')

                    if len(columns) > 0:
                         key = columns[0].text.lower().strip()
                         value = columns[1].text.strip()

                         price_incentive[key] = value

               # print(price_incentive)
          return price_incentive
     
     except Exception as e:
          print(f"Error while getting the prices and incentives : {e}")



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
               
          # print(len(amenities_list))
          return amenities_list
     except Exception as e:
          print(f"Error occured while getting Amenities : {e}")
     
     
def floor_plan(soup):
     try:
          floor_pln_container = soup.find("div", id = "floorplans")
          if floor_pln_container:

               # for 1_bed
               floor_pln_boxes = floor_pln_container.find_all("div", class_ = "tab-pane")
               floor_pln_keys = floor_pln_container.find_all('li')
               
               for box, key in zip(floor_pln_boxes, floor_pln_keys):
                    floor_pln_items = box.find_all("div", class_ = "tab-pane-item")
                    floor_pln_key = key.text.strip()
                    # print(len(floor_pln_items))
                    floor_pln = {}
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
                    
                    floor_pln[floor_pln_key.lower()] =  floor_pln_list
               
               return floor_pln
          
     except Exception as e:
          print(f"Error while getting the floor plans : {e}")
     
def last_updated(soup):
     try:
          last_updated_container = soup.find("div", class_ = "condo-breadcrumbs")
          if last_updated_container:
               last_updated_element = last_updated_container.find('p', class_ = "fst-italic m-0 p-0")
               last_updated_date = last_updated_element.text.strip().replace('Last Updated:', '')
               
          return last_updated_date
     
     except Exception as e:
          print(f"Error while getting last updated date : {e}")
     
def functions_handler(soup, *functions):
     results = []
     for func in functions:
          results.append(func(soup))
     
     return results


def url_handler(df):
     urls = df['link'].head(5)
     # urls = ['https://precondo.ca/high-line-condos/?authenticated=96721']
     
     
     for i,url in enumerate(urls):
          print(i+1, url)
          soup = soup_creator(url)
          data = []
          
          if not soup:
               print(f"Failed to fetch data for {url}")
               continue
          
          img_src, title_location, overview, price_and_incentive, description, amenities, floor_pln, last_update =  functions_handler(soup, image, title_and_location, Overview, price_and_incentives, details, amenity, floor_plan, last_updated)
          
          row = {
               
               'url' : url,
               'img_src' : img_src,
               'title' : title_location[0],
               'location' : title_location[1],
               'price' : title_location[2],
               'price_range' : price_and_incentive['Price Range'] if len(price_and_incentive['Price Range']) > 0 else None,
               'one_bed_starting_from' : price_and_incentive['1 Bed Starting From'].split()[1],
               'one_bed_starting_from_unit' : price_and_incentive['1 Bed Starting From'].split()[0],
               'two_bed_starting_from' : price_and_incentive['2 Bed Starting From'].split()[1],
               'two_bed_starting_from_unit' : price_and_incentive['2 Bed Starting From'].split()[0],
               'price_per_sqft' : price_and_incentive['Price Per Sqft'].split()[1],
               'avg_price_per_sqft' : price_and_incentive['Avg Price Per Sqft'].split()[1] if len(price_and_incentive['Avg Price Per Sqft'].split()[1]) > 1 else None,
               'avg_price_per_sqft_unit' : price_and_incentive['Avg Price Per Sqft'].split()[0] if len(price_and_incentive['Avg Price Per Sqft'].split()[1]) > 0 else None,
               'city_avg_price_per_sqft' : price_and_incentive['City Avg Price Per Sqft'].split()[1] if len(price_and_incentive['City Avg Price Per Sqft'].split()) > 1 else None,
               'city_avg_price_per_sqft_unit' : price_and_incentive['City Avg Price Per Sqft'].split()[0] if len(price_and_incentive['City Avg Price Per Sqft'].split()) > 0 else None,
               'development_levies' : price_and_incentive['Development Levies'],
               'parking_cost' : price_and_incentive['Parking Cost'].split()[1] if len(price_and_incentive['Parking Cost'].split()) > 1 else None,
               'parking_cost_unit' : price_and_incentive['Parking Cost'].split()[0] if len(price_and_incentive['Parking Cost'].split()) > 0 else None,
               'parking_maintenance' : price_and_incentive['Parking Maintenance'].split()[1] if len(price_and_incentive['Parking Maintenance'].split()) > 1 else None,
               'parking_maintenance_unit' : price_and_incentive['Parking Maintenance'].split()[0] if len(price_and_incentive['Parking Maintenance'].split()) > 1 else None,
               'assignment_fee_free' : price_and_incentive['Assignment Fee Free'],
               'storage_cost' : price_and_incentive['Storge Cost'].split()[1] if len(price_and_incentive['Storge Cost'].split()) > 1 else None,
               'storage_cost_unit' : price_and_incentive['Storge Cost'].split()[0] if len(price_and_incentive['Storge Cost'].split()) > 0 else None,
               'incentives' : price_and_incentive['Incentives'],
               'deposit_structure' : price_and_incentive['Deposit Structure']
               
          }
          
          data.append(row)
          
     df = pd.DataFrame(data)
          
     return df
          
          
     
def main():
     urls_df = pd.read_csv('api_urls.csv')
     
     df = url_handler(urls_df)
     
     df.to_csv('detail.csv')
     
     
if __name__ == '__main__':
     main()


