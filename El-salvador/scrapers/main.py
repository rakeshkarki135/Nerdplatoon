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
     driver.set_page_load_timeout(180)
     driver.maximize_window()
     return driver


def generate_unique_uuid(df):
     while True:
          uuids = uuid.uuid4()
          
          if uuids not in df['uuid'].values:
               return uuids

def detailScraper(i, df, url, driver):
     
     driver.get(url)
     
     soup = BeautifulSoup(driver.page_source, 'lxml')

     try:
          WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-10.sm-col-10.md-col-10.lg-col-8.mx-auto.body-text.justify.relative')))
     
     except Exception as e:
          pass
     
     # for urls
     df.at[i, 'link'] = url
     
     
     try:
          main_container = soup.find('div', class_='col-10 sm-col-10 md-col-10 lg-col-8 mx-auto body-text justify relative')

     except Exception as e:
          pass

     try:
          # for the title and code
          if main_container:
               
               title_element = main_container.find('div', class_='md-col md-col-8 px2 remax-gray2')
               
               if title_element:
                    title = title_element.find('h1', class_ = 'mb1').get_text(strip=True) if title_element else None
                    df.at[i, 'title'] = title
                    
                    code  = title_element.find('p', class_ = 'md-right').get_text(strip=True) if title_element else None
                    df.at[i, 'code_number'] = code
          
     except Exception as e:
          pass
          
          
     # for country
     df.at[i, 'country'] = 'El Salvador'
     
     # for uuid 
     uids = uuid.uuid4()
     df.at[i, 'uuid'] = generate_unique_uuid(df)
     
     
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
          
          
     except Exception as e:
          pass
     
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
               
               
     except Exception as e:
          pass
          
          
     room = {}
     try:
          room_details_element = main_container.find('div', class_='clearfix mb2')
          
          if room_details_element:
               boxes = room_details_element.find_all('div', class_='col col-6 md-col-4 lg-col-2 py1 px2 center')
               
               for box in boxes:
                    key_element = box.find('p', class_='text-80')
                    value_element = box.find('div', class_='inline-block text-80')
                    
                    if key_element and value_element:
                         key = key_element.text.strip()
                         value = value_element.text.strip().replace('x', '')
                         
                         if key == 'Area of Land':
                              value = value.replace('v2', '')
                              df.at[i, 'area_square_vara'] = float(value)
                         
                         elif key == 'Construction Area':
                              df.at[i, 'construction_area'] = value.replace('m2', '')
                         
                         elif key == 'Bathrooms':
                              datas = value.split()
                              df.at[i, 'full_baths'] = datas[0] if len(datas) > 0 else None
                              df.at[i, 'half_baths'] = datas[1].replace('½', '1') if len(datas) > 1 else None
                         
                         elif 'Full baths' in key or 'half baths' in key:
                              df.at[i, 'full_baths'] = value
                              half_bath = re.findall(r'\d+', key)
                              df.at[i, 'half_baths'] = int(half_bath[0]) if half_bath else None
                         
                         elif key == 'Rooms':
                              df.at[i, 'bedrooms'] = value
                         
                         elif key == 'Parking Lot':
                              df.at[i, 'parking'] = value

               # Nested try-except for levels extraction
               try:
                    levels_element = room_details_element.find('div', class_='col col-6 md-col-4 lg-col-1 py1 px1 center')
                    
                    if levels_element:
                         levels = levels_element.get_text(strip=True)
                         
                         if levels:
                              levels = re.findall(r'\d+', levels)
                              df.at[i, 'levels'] = levels[0] if levels else None

               except Exception as e:
                    pass

     except Exception as e:
          pass

          
     try:
          type_element = room_details_element.find('div', class_ = 'col col-12 sm-col-12 lg-col-1 py1 px2 center')
          privacy_element = type_element.find('p', class_ = 'text-80') if type_element else None
          
          if privacy_element:
               privacy = privacy_element.text.strip() 
               
          else:
               privacy = None
               
          df.at[i, 'privacy'] = privacy
          
          
     except Exception as e:
          pass
          
     
     # for description
     try:
          description_element = main_container.find('div', class_ = 'md-col md-col-8 px2 mb4')
          
          if description_element:
               description = description_element.find_all(string=True, recursive=False)
          
          df.at[i, 'description'] = str(''.join(description).strip())
          
          
     except Exception as e:
          pass
          
     
     # for image urls
     
     WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.flex.items-center.carousel.mb1')))

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
                         
               df.at[i, 'img_src'] = str(img_urls) if img_urls else None
     
     except Exception as e:
          pass

     created_time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
     df.at[i, 'created_at'] = created_time
     uploaded_time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
     df.at[i, 'updated_at'] = uploaded_time
     
     return df

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
     
     new_df = pd.DataFrame(columns=['link','uuid','phone','previous_price','price_unit'])
     
     mainScraper(new_df, driver)
     
     driver.quit()
     
     print('Data Scraping Completed')
     
     df = new_df.dropna(subset=['title','img_src'])
     
     df.to_csv('detail.csv', index=False)
          


if __name__ == '__main__':
     main()


