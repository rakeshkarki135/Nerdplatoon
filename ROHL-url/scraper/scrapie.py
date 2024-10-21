from selenium import webdriver 
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC                 
import pandas as pd              
import os    
import json        

def driverInitializer():
     driver = webdriver.Chrome()
     driver.maximize_window()
     return driver

def loadCSV(filePath):
     return pd.read_csv(filePath)

def get_current_directory():
     return os.path.dirname(os.path.abspath('C:/Users/LENOVO/OneDrive/Desktop/scraping/nerdplatoon/ROHL-url/scraper/'))

def detailScraper(driver, wait, url):
     driver.get(url)
     
     # Scrape detail text
     detail = driver.find_element(By.ID, "slick-slide00")
     detail_txt = detail.text.strip() if detail else 'Nan'

     # Scrape features
     features_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".plmr-c-banner-list-items__content.plmr-c-general-content.js-product-features")))
     features = features_box.find_element(By.TAG_NAME, 'ul').text if features_box else 'Nan'

     # Scrape specifications
     specification_container = driver.find_element(By.CLASS_NAME, 'plmr-c-additional-product-specs')
     boxes = specification_container.find_elements(By.CLASS_NAME, 'plmr-c-featured-product-specs__item')

     specification = {}
     for box in boxes:
          spec_name = box.find_element(By.CLASS_NAME, 'plmr-c-featured-product-specs__item-text').text.strip()
          spec_value = box.find_element(By.CLASS_NAME, 'plmr-c-featured-product-specs__item-name').text.strip()
          specification[spec_name] = spec_value

     # Scrape finishes
     finishes = []
     finish_container = driver.find_element(By.CSS_SELECTOR, '.plmr-c-product-info__finishes.js-product-finishes-list')
     li_items = finish_container.find_elements(By.TAG_NAME, 'li') if finish_container else None
     
     for item in li_items:
          sku = item.get_attribute('data-sku')
          a_tag = item.find_element(By.TAG_NAME, 'a')
          link = a_tag.get_attribute('href') if a_tag else 'Nan'
          name_cont = item.find_element(By.CSS_SELECTOR, '.plmr-c-finishes-nav__finish-name')
          hidden_name = driver.execute_script('return arguments[0].textContent;', name_cont)
          name = hidden_name.strip() if hidden_name else 'Nan'
          
          finish = {
               'title': name,
               'link': link,
               'sku': sku
          }
          finishes.append(finish)

     # Scrape file link
     file_con = driver.find_element(By.CLASS_NAME, "plmr-c-product-info-condensed__links")
     file_link = file_con.find_element(By.TAG_NAME, 'a') if file_con else None
     file = file_link.get_attribute('href') if file_link else 'Nan'

     return detail_txt, features, specification, finishes, file

def update_csv(df,i,detail_txt, features, specification, finishes, file):
     df.at[i, 'Detail'] = detail_txt
     df.at[i, 'Features'] = features
     df.at[i, 'Specifications'] = json.dumps(specification)
     df.at[i, 'Finishes'] = json.dumps(finishes)
     df.at[i, 'File'] = file
     
     
def main():
     # initializing the driver
     driver = driverInitializer()
     
     wait = WebDriverWait(driver, 15)
     
     # load csv
     current_dir = get_current_directory()
     urls_csv_path = os.path.join(current_dir, 'urls.csv')
     detail_csv_path = 'C:/Users/LENOVO/OneDrive/Desktop/scraping/nerdplatoon/ROHL-url/detail.csv'
     
     url_df = loadCSV(urls_csv_path)
     detail_df = loadCSV(detail_csv_path)
     
     for i,link in enumerate(url_df['URL']):
          print(i,link)
          
          detail, features, specification, finishes, file = detailScraper(driver, wait, link)
          
          update_csv(detail_df, i, detail, features, specification, finishes, file)  
          
     
     detail_df.to_csv(detail_csv_path, index=False)
     
     driver.quit()
     
     
if __name__ == '__main__':
     main()