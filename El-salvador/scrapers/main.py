import uuid
import pandas as pd
from bs4 import BeautifulSoup
import re  
import datetime 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
     

def driverInitialization():
     driver = webdriver.Chrome()
     driver.maximize_window()
     return driver

def detailScraper(i, df, url, driver):
     
     driver.get(url)
     
     soup = BeautifulSoup(driver.page_source, 'lxml')

     try:
          WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'relative')))
          WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-10.sm-col-10.md-col-10.lg-col-8.mx-auto.body-text.justify.relative')))
     
     except Exception as e:
          print(f'Error Occured : {e}')
     
     # for urls
     df.at[i, 'links'] = url
     
     
     try:
          main_container = soup.find('div', class_='col-10 sm-col-10 md-col-10 lg-col-8 mx-auto body-text justify relative')

     except Exception as e:
          print(f'Error Occured while getting main container: {e}')

     try:
          # for the title and code
          if main_container:
               
               title_element = main_container.find('div', class_='md-col md-col-8 px2 remax-gray2')
               
               if title_element:
                    title = title_element.find('h1', class_ = 'mb1').get_text(strip=True) if title_element else None
                    df.at[i, 'title'] = title
                    
                    code  = title_element.find('p', class_ = 'md-right').get_text(strip=True) if title_element else None
                    df.at[i, 'code'] = code
               else:
                    print("Title Element is not Found")
          else:
               print("Main_container is not Found")
          
     except Exception as e:
          print(f'Error Occured while getting title and code : {e}')
          
          
     # for country
     df.at[i, 'country'] = 'El Salvador'
     
     # for uuid 
     uids = uuid.uuid4()
     df.at[i, 'uuid'] = uids
     
     
     try:
          # for the location and property type
          location_element = title_element.find_all('li', class_ = 'inline-block') if title_element else None
          
          if location_element:
               location = location_element[0].get_text(strip=True) if location_element else None
               df.at[i, 'location'] = location
               
               property_type = location_element[1].get_text(strip=True) if location_element else None
               df.at[i, 'property_type'] = property_type
               
               type = location_element[2].get_text(strip = True) if location_element else None
               df.at[i, 'type'] = type
          else:
               print("Location Element is not Found")
          
     except Exception as e:
          print(f'Error Occured while getting location and property type: {e}')
     
     # for price
     try: 
          if main_container:
               price_element = main_container.find('div', class_ = 'md-col md-col-4 px2')
               if price_element:
                    price = price_element.find('div', class_ = 'bg-remax-red white p1 center text-150 rounded').get_text(strip=True)
                    
                    if price:
                         price = re.sub(r'[\$,/m2]','', price)
                    else:
                         price = None
                    
                    df.at[i, 'price'] = price
               else:
                    print('Price Element is not Found')
          else:
               print("Main container is not Found")
               
     except Exception as e:
          print(f'Error Occured while getting price: {e}')
          
     
     room = {}
     try:
          room_details_element = main_container.find('div', class_ = 'clearfix mb2')
          
          if room_details_element:
               boxes = room_details_element.find_all('div', class_ = 'col col-6 md-col-4 lg-col-2 py1 px2 center')
               for box in boxes:
                    key_element = box.find('p', class_ = 'text-80')
                    value_element = box.find('div', class_ = 'inline-block text-80')
                    
                    if key_element and value_element:
                         key = key_element.text.strip()
                         value = value_element.text.strip().replace('x', '')
                         # value = re.findall(r'\d+', value)[0]
                         
                         if key == 'Area of Land':
                              df.at[i, 'area_square_vara'] = value.replace('v2', '')
                                   
                         elif key == 'Construction Area':
                              df.at[i, key] = value.replace('m2', '')
                              
                         elif key == 'Bathrooms':
                              datas = value.split()
                              df.at[i, 'full_bathroom'] = datas[0] if len(datas) > 0 else None
                              
                              df.at[i, 'half_bathroom'] = datas[1].replace('½','1') if len(datas) > 1 else None
                              
                         elif 'Full baths' in key or 'half baths' in key:
                              df.at[i, 'full_bathroom'] = value
                              
                              half_bath = re.findall(r'\d+', key)
                              
                              df.at[i, 'half_bathroom'] = int(half_bath[0])
                              
                         else:
                              df.at[i, key] = value
                    
                         
                    else:
                         print("Missing key_element or value_element")
                         
               try:
                    levels_element = room_details_element.find('div', class_ = 'col col-6 md-col-4 lg-col-1 py1 px1 center')
                    
                    if levels_element:
                         levels = levels_element.get_text(strip=True)
                         levels = re.findall(r'\d+', levels)
                    else:
                         levels = None
                         
                    df.at[i, 'levels'] = levels[0]
                    
               except Exception as e:
                    print(f"Error Occured while getting levels : {e}")
               
          else:
               print("Room Details element not Found")
               
     except Exception as e:
          print(f'Error Occured while getting room_details : {e}')
          
          
     try:
          type_element = room_details_element.find('div', class_ = 'col col-12 sm-col-12 lg-col-1 py1 px2 center')
          privacy_element = type_element.find('p', class_ = 'text-80') if type_element else None
          
          if privacy_element:
               privacy = privacy_element.text.strip() 
               
          else:
               privacy = None
               
          df.at[i, 'privacy'] = privacy
          
          
     except Exception as e:
          print(f'Error Occured while getting privacy : {e}')
          
     
     # for description
     try:
          description = main_container.find('div', class_ = 'md-col md-col-8 px2 mb4').get_text(strip=True) if main_container else None
          
          df.at[i, 'description'] = str(description)
          
     except Exception as e:
          print(f'Error Occured while getting description: {e}')
          
     
     # for image urls
     
     WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.flex.items-center.carousel.mb1')))

     try:
          img_urls = []
          
          carousel_element = main_container.find('div', class_ = 'flex items-center carousel mb1') 
          
          if carousel_element:
               items = carousel_element.find_all('li') 
               
               for item in items:
                    img = item.find('a')
                    
                    if img and img.has_attr('href'):
                         img_url = img.get('href')
                         
                         if img_url not in img_urls:
                              img_urls.append(img_url)
                    
                    else:
                         img_url = None
                         
               df.at[i, 'image_urls'] = str(img_urls) if img_urls else None
          else:
               print('Carousel Element not Found')
     
     except Exception as e:
          print(f'Error Occured while getting images : {e}')

     created_time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
     df.at[i, 'created_time'] = created_time
     uploaded_time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
     df.at[i, 'uploaded_time'] = uploaded_time

def mainScraper(new_df, driver):
     
     urls_df = pd.read_csv('urls.csv')
     urls = urls_df['urls']
     
     for i,url in enumerate(urls):
          print(i, url)
          
          try:
               detailScraper(i, new_df, url,  driver)
          except Exception as e:
               print(f'Error Occured in link : {url}')



def main():
     
     driver = driverInitialization()
     
     new_df = pd.DataFrame(columns=['links'])
     
     mainScraper(new_df, driver)
     
     driver.quit()
     
     print('Data Scraping Completed')
     
     df = new_df.dropna(subset=['title','image_urls'])
     
     df.to_csv('detail.csv', index=False)
          


if __name__ == '__main__':
     main()