from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd    
import os 
import json



driver = webdriver.Chrome()

wait = WebDriverWait(driver, 15)

current_dir = os.path.dirname(os.path.abspath('C:/Users/LENOVO/OneDrive/Desktop/scraping/nerdplatoon/ROHL-url/scraper/'))

csv_file_path = os.path.join(current_dir, 'urls.csv')

df = pd.read_csv(csv_file_path)

csv_file = pd.read_csv('C:/Users/LENOVO/OneDrive/Desktop/scraping/nerdplatoon/ROHL-url/detail.csv')

driver.maximize_window()

# print(data)
for i,link in  enumerate(df['URL']):
     print(link)
     driver.get(link)
     
     try:
          cookie_banner = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'plmr-c-cookie-notification')))
          cookie_close_button = cookie_banner.find_element(By.TAG_NAME, 'button')
          cookie_close_button.click()
          
     except:
          print("No cookie banner found")
     
     # detail = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'plmr-c-carousel-mega-title-copy__item-content')))
     length = driver.find_element(By.CSS_SELECTOR, '.plmr-c-carousel-mega-title-copy__arrow.slick-next.slick-arrow').text.strip()
     length = int(length)
     print(type(length))
     
     detail = []
     

     for i in range(length):
          
          carousel_content_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.plmr-c-carousel-mega-title-copy__item.slick-slide.slick-current.slick-active')))
          
          if carousel_content_container:
               # Extract content within the container
               carousel_content = carousel_content_container.find_element(By.CLASS_NAME, 'plmr-c-carousel-mega-title-copy__item-content')
               
               # Extract and print the text if content exists
               if carousel_content:
                    carousel_text = [carousel_content.text.strip()]
                    print(i, carousel_text)
                    detail.append(carousel_text)
                    
          
          # Locate the next button container
          carousel_external_container = driver.find_element(By.CLASS_NAME, 'plmr-c-carousel-mega-title-copy__nav-container')
          
          carousel_button_container = carousel_external_container.find_element(By.CLASS_NAME, 'plmr-c-carousel-mega-title-copy__nav-bar') if carousel_external_container else None
          
          if carousel_button_container:
               next_button = carousel_button_container.find_element(By.CSS_SELECTOR, '.plmr-c-carousel-mega-title-copy__arrow.slick-next.slick-arrow')
                    
               # Click the next button if it exists
               driver.execute_script('arguments[0].scrollIntoView();', next_button)
               
               # click using js to avoid interception
               driver.execute_script("arguments[0].click();", next_button)
               
          else:
               break
          
     # print(detail)
          
     break
     
     # detail = driver.find_element(By.ID, "slick-slide00")
     
     # detail_txt = detail.text.strip() if detail else 'Nan'
     # print(detail_txt)
     
#      features_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".plmr-c-banner-list-items__content.plmr-c-general-content.js-product-features")))
     
#      features = features_box.find_element(By.TAG_NAME, 'ul').text if features_box else 'Nan'
     
#      specification_container  = driver.find_element(By.CLASS_NAME, 'plmr-c-additional-product-specs')
     
#      boxes = specification_container.find_elements(By.CLASS_NAME, 'plmr-c-featured-product-specs__item')
     
#      specification = {}
     
#      for box in boxes:
          
#           spec_name = box.find_element(By.CLASS_NAME, 'plmr-c-featured-product-specs__item-text').text.strip()
          
#           spec_value = box.find_element(By.CLASS_NAME, 'plmr-c-featured-product-specs__item-name').text.strip()
          
#           specification[spec_name] = spec_value
     
#      # print(specification)
     
#      finish_container = driver.find_element(By.CSS_SELECTOR,'.plmr-c-product-info__finishes.js-product-finishes-list')
     
#      li_items = finish_container.find_elements(By.TAG_NAME, 'li') if finish_container else None   
     
#      finishes = []
     
#      for item in li_items:
#           sku = item.get_attribute('data-sku')
#           a_tag = item.find_element(By.TAG_NAME,'a')
#           link = a_tag.get_attribute('href') if a_tag else 'Nan'
#           name_cont = item.find_element(By.CSS_SELECTOR,'.plmr-c-finishes-nav__finish-name')
#           hidden_name = driver.execute_script('return arguments[0].textContent;',name_cont)
#           name = hidden_name.strip() if hidden_name else 'Nan'
          
#           finish = {
#                'title':name,
#                'link':link,
#                'sku':sku
#           }
          
#           finishes.append(finish)
          
#      file_con = driver.find_element(By.CLASS_NAME, "plmr-c-product-info-condensed__links")
#      file_link = file_con.find_element(By.TAG_NAME, 'a') if file_con else None
#      file = file_link.get_attribute('href') if file_link else 'Nan'
#      # print(file)
     
#      csv_file.at[i, 'Detail'] = detail_txt
#      csv_file.at[i, 'Features'] = features
#      csv_file.at[i, 'Specifications'] = json.dumps(specification)
#      csv_file.at[i, 'Finishes'] = json.dumps(finishes)
#      csv_file.at[i, 'File'] = file
     
# csv_file.to_csv('C:/Users/LENOVO/OneDrive/Desktop/scraping/nerdplatoon/ROHL-url/detail.csv', index=False)

driver.quit()
