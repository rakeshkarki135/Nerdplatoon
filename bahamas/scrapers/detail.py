import re 
import pandas as pd    
import uuid
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC         

def driverInitialization():
     driver = webdriver.Chrome()
     driver.maximize_window()
     return driver

def unique_uuid_Generator(df):
     while True:
          new_uuid = str(uuid.uuid4())
          
          if new_uuid  not in df['uuid']:
               return new_uuid
     
def detail_Scraper(url, driver, i, df):
     driver.get(url)
     WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.grid.global-content.js-global-content')))
     
     soup = BeautifulSoup(driver.page_source, 'lxml')
     
     # for link
     df.at[i, 'link'] = url
     
     # for uuid
     df.at[i, 'uuid'] = unique_uuid_Generator(df)
     
     # for title and location
     try:
          main_container = soup.find('div', class_ = 'grid global-content js-global-content')
          if  main_container:
               head_con = soup.find('div', id='listingtitle')
               
               if head_con:
                    # title
                    title_element = head_con.find('span')
                    if title_element:
                         title = title_element.get_text(strip=True)
                    else:
                         title = None
                    df.at[i, 'title'] = title 
                    
                    # address
                    address_element = head_con.find('span', class_ = 'c-address')
                    if address_element:
                         address = address_element.get_text(strip=True)
                    else:
                         address = None
                    df.at[i, 'location'] = address  
                    
                    # for price and price unit
                    price_con = head_con.find('div', class_ = 'c-price')
                    if price_con:
                         price_element = price_con.find('span')
                         
                         # price
                         if price_element:
                              price = price_element.get_text(strip=True)
                              price = ''.join(re.findall(r'\d+', price))
                         else:
                              price = None
                         df.at[i, 'price'] = price
                         
                         # price unit
                         priceUnit_element = price_con.find('span', class_ = 'price__rental-frequency')
                         if priceUnit_element:
                              price_unit = priceUnit_element.get_text(strip=True)
                         else:
                              price_unit = None
                         df.at[i, 'price_unit'] = price_unit     
     except Exception as e:
          print(f'Error while getting Head Details : {e}')
          
          
     # for type
     property_type = url.split('/')[4]
     df.at[i, 'type'] = property_type   
          
          
     # for propertyDetail
     try:
          main_propDetail_con = soup.find('div', id='listinginfo')
          if main_propDetail_con:
               propDetail_con = main_propDetail_con.find('div', class_='grid__item')
               
               if propDetail_con:
                    propDetail_boxes = propDetail_con.find_all('div', {'data-same-height-group':'listinginfo'})

                    for box in propDetail_boxes:
                         key_element = box.find('dt', class_ = 'listing-info__title')
                         value_element = box.find('dd', class_ = 'listing-info__value')
                         
                         if key_element and value_element:
                              key = key_element.get_text(strip=True)
                              value = value_element.get_text(strip=True)
                              
                              if key in ['Full Baths', 'Full Bath']:
                                   df.at[i, 'Full Baths'] = value
                              elif key in ['Partial Baths', 'Partial Bath']: 
                                   df.at[i, 'Partial Baths'] =  value
                              elif key in ['Bedrooms','Bedroom']:
                                   df.at[i, 'Bedrooms'] = value
                              else:
                                   if key == 'Interior':
                                        value = ''.join(re.findall(r'\d+', value))
                                   if key == 'Exterior':
                                        value = value.replace('Acres', '')
                                   df.at[i, key] = value
                                        
     except Exception as e:
          print(f'Error while getting  Property Details  : {e}')
          
          
     # for amenities
     amnities_list = []
     try:
          amnties_main_con = soup.find('div', id = 'listingpropertydescription')
          if amnties_main_con:
               amnties_elements = amnties_main_con.find_all('span', class_ = 'prop-description__amenities-list-item-text')
               # print(len(amnties_list))
               if amnties_elements:
                    amnities_list.extend([item.get_text(strip=True) for item in amnties_elements])
                    
               # for features
               features = {}
               features_con = amnties_main_con.find('div', class_ = 'prop-description__features-list')
               if features_con:
                    features_boxes = features_con.find_all('div', class_ = 'grid__item')
                    for box in features_boxes:
                         key_element = box.find('dt')
                         value_element = box.find('dd')
                         
                         if key_element and value_element:
                              key = key_element.get_text(strip=True)
                              value = value_element.get_text(strip=True)
                              features[key] = value
                              
                    df.at[i, 'new_features'] = str(features)
               
     except Exception as e:
          print(f'Error while getting Amenities  : {e}')
     
          
     # for description
     if amnties_main_con:
          try:
               description_con = amnties_main_con.find('div', class_ = 'p')
               if description_con:
                    description = description_con.get_text(strip=True)
               else:
                    description = None
               df.at[i, 'about'] = description
               
          except Exception as e:
               print(f'Error while getting Description : {e}')
          
          # for exterior container 
          try:
               exterior_con = amnties_main_con.find('div', class_ = 'prop-description__details')
          except Exception as e:
               print(f'Error while getting exterior Container : {e}')
     
     
     # for proprety exterior details
     if exterior_con:
          try:
               exterior_boxes = exterior_con.find_all('div', class_ = 'grid__item')
               # print(len(exterior_boxes))
               for box in exterior_boxes:
                    ext_title = box.find('h3', class_ = 'prop-description__title').get_text(strip=True)
                    dl_con = box.find('dl')
                    
                    exterior_details = {}
                    
                    key_elements = dl_con.find_all('dt') if dl_con else None
                    value_elements = dl_con.find_all('dd')if dl_con else None
                    
                    for x,y in zip(key_elements,value_elements):
                         key = x.get_text(strip=True)
                         value = y.get_text(strip=True)
                         
                         if key == 'Amenities':
                              amnities_list.append(value)
                         else:
                              exterior_details[key] = value
                         
                    if ext_title == 'Exterior':
                         df.at[i, 'exterior_details'] = str(exterior_details)
                    elif ext_title == 'Interior':
                         df.at[i, 'interior_details'] = str(exterior_details)
                    else:
                         df.at[i, ext_title] = str(exterior_details)
                         
          except Exception as e:
               print(f'Error while getting Exterior Details  : {e}')
     
     
     # inserting amenities values
     df.at[i, 'amenities'] = str(amnities_list) if amnities_list else None
     
     
     # for image_urls
     img_urls = []
     try:
          img_carousel_con = soup.find('div', id = 'detail_photos_carousel_placeholder')
          if img_carousel_con:
               img_con = img_carousel_con.find('div', class_ = 'runner')
               
               if img_con:
                    img_boxes = img_con.find_all('img')
                    
                    for box in img_boxes:
                         urls = box.get('data-image-url-format', None)
                         img_urls.append(urls)
                    
                    df.at[i, 'img_src'] = str(img_urls) if img_urls else None
                    
     except Exception as e:
          print(f'Error while getting image urls : {e}')
     
     
     # for latitude and longitude
     try:
          multimedia_con = driver.find_element(By.ID, 'multimedia_details' )
          if multimedia_con:
               position_con = multimedia_con.find_element(By.ID, 'map_tab')
               
               if position_con:
                    position_con.click()
                    position_element = multimedia_con.find_element(By.NAME, 'daddr')
                    
                    if position_element:
                         position = position_element.get_attribute('value')
                         
                         if position:
                              position_parts = position.split(',')
                              # for flag
                              if len(position_parts) >= 2:
                                   df.at[i, 'location_flag'] = 1
                              else:
                                   df.at[i, 'location_flag'] = 0
                                   
                              lat = position_parts[0]
                              df.at[i, 'lat'] = lat
                              lon = position_parts[1]
                              df.at[i, 'lon'] = lon

     except Exception as e:
          print(f'Error while getting multimedia container : {e}')
     
     # for created_at
     df.at[i, 'created_at'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
     
     df.at[i, 'updated_at'] = None
     
     df.at[i, 'deleted_at'] = None
     
     return df
     

def url_Extractor(driver, df):
          link_df = pd.read_csv('urls.csv')
          urls = link_df['link']
          
          for i,url in enumerate(urls):
               try:
                    print(i, url)
                    detail_Scraper(url, driver, i, df)
               except Exception as e:
                    print(f'Error in link -----> {url} : {e}')

def main():
     driver = driverInitialization()
     
     df = pd.DataFrame(columns=['link','uuid'])
     
     url_Extractor(driver, df)    
     
     driver.quit()
     
     df.to_csv('details.csv', index=False)
     
     print("Scraping Completed")
     
     
if __name__ == '__main__':
     main()
     
     