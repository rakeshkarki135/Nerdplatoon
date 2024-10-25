from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import re       

def driverInitialization():
     driver = webdriver.Chrome()
     driver.maximize_window()
     return driver

def detailScraper(i, df, url, driver):
     
     driver.get(url)
     
     soup = BeautifulSoup(driver.page_source, 'lxml')


     try:
          WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'relative')))
     
     except Exception as e:
          print(f'Error Occured : {e}')
     
     # for urls
     df.loc[i, 'LINKS'] = url
     
     
     try:
          main_container = soup.find('div', class_='col-10 sm-col-10 md-col-10 lg-col-8 mx-auto body-text justify relative')

     except Exception as e:
          print(f'Error Occured while getting main container: {e}')

     try:
          # for the title and code
          title_element = main_container.find('div', class_='md-col md-col-8 px2 remax-gray2')
          
          title = title_element.find('h1', class_ = 'mb1').get_text(strip=True) if title_element else None
          df.loc[i, 'TITLE'] = title
          
          code  = title_element.find('p', class_ = 'md-right').get_text(strip=True) if title_element else None
          df.loc[i, 'CODE'] = code
          
     except Exception as e:
          print(f'Error Occured while getting title and code : {e}')
          
     
     try:
          # for the location and property type
          location_element = title_element.find_all('li', class_ = 'inline-block') if title_element else None
          
          location = location_element[0].get_text(strip=True) if location_element else None
          df.loc[i, 'LOCATION'] = location
          
          property_type = location_element[1].get_text(strip=True) if location_element else None
          df.loc[i, 'PROPERTY TYPE'] = property_type
          
          type = location_element[2].get_text(strip = True) if location_element else None
          df.loc[i, 'TYPE'] = type
          
     except Exception as e:
          print(f'Error Occured while getting location and property type: {e}')
          
     
     # for price
     try: 
          price_element = main_container.find('div', class_ = 'md-col md-col-4 px2') if main_container else None
          price = price_element.find('div', class_ = 'bg-remax-red white p1 center text-150 rounded').get_text(strip=True) if price_element else None
          
          if price:
               if '$' in price:
                    price = re.sub(r'[$,]', '', price)
                    df.loc[i, 'PRICE'] = price
          else:
               price = None
          
     except Exception as e:
          print(f'Error Occured while getting price: {e}')
          
     
     room = {}
     try:
          room_details_element = main_container.find('div', class_ = 'clearfix mb2')
          boxes = room_details_element.find_all('div', class_ = 'col col-6 md-col-4 lg-col-2 py1 px2 center')
          for box in boxes:
               key = box.find('p', class_ = 'text-80').get_text(strip=True) 
               value = box.find('div', class_ = 'inline-block text-80').text.strip().replace('x', '')
               
               if key == 'Area of Land':
                         df.loc[i, key] = value.replace('v2', '')
                         
               if key == 'Construction Area':
                    df.loc[i, key] = value.replace('m2', '')
                    
               if key == 'Bathrooms':
                    datas = value.split()
                    df.loc[i, 'FULL BATHROOM'] = datas[0]
                    
                    df.loc[i, 'HALF BATHROOM'] = datas[1]

     except Exception as e:
          print(f'Error Occured while getting room_details : {e}')
          
     try:
          type_element = room_details_element.find('div', class_ = 'col col-12 sm-col-12 lg-col-1 py1 px2 center')
          privacy_element = type_element.find('p', class_ = 'text-80') if type_element else None
          
          if price_element:
               privacy = privacy_element.text.strip() 
               
          else:
               privacy = None
               
          df.loc[i, 'PRIVACY'] = privacy
          
          
     except Exception as e:
          print(f'Error Occured while getting privacy : {e}')
          
     
     # for description
     try:
          description = main_container.find('div', class_ = 'md-col md-col-8 px2 mb4').get_text(strip=True) if main_container else None
     
     except Exception as e:
          print(f'Error Occured while getting description: {e}')
          
     
     try:
          img_urls = []
          carousel_element = main_container.find('div', class_ = 'flex items-center carousel mb1') 
          
          if carousel_element:
               items = carousel_element.find_all('li', class_ = 'bx-clone') 
               
               for item in items:
                    img = item.find('img')
                    if img:
                         img_url = img['src']
                         
                         if img_url not in img_urls:
                              img_urls.append(img_url)
                    
                         
                    else:
                         img_url = None
          
          df.loc[i, 'IMAGE URLS'] = ', '.join(img_urls) 
     
     except Exception as e:
          print(f'Error Occured while getting images : {e}')


     
def main():
     
     driver = driverInitialization()
     
     urls_df = pd.read_csv('urls.csv')
     
     new_df = pd.DataFrame(columns=['LINKS'])
     
     for i,url in enumerate(urls_df['urls']):
          print(i, url)
          
          detailScraper(i, new_df, url, driver)
     
     driver.quit()
     
     print('Data Scraping Completed')
     
     new_df.to_csv('detail.csv', index=False)
          

if __name__ == '__main__':
     main()