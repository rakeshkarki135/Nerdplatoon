from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC       
import pandas as pd                     


def driverInitialialization():
     driver = webdriver.Chrome()
     driver.maximize_window()
     return driver

def urlExtractor(driver, url):
     links = []
     
     while True:
          driver.get(url)
          
          out_container = driver.find_element(By.CSS_SELECTOR, '.clearfix.mt4')
          
          inner_container = out_container.find_element(By.CSS_SELECTOR, '.col-12.sm-col-10.md-col-10.lg-col-8.mx-auto') if out_container else None 
          
          main_container = inner_container.find_element(By.CLASS_NAME, 'clearfix') if inner_container else None
          
          boxes = main_container.find_elements(By.CSS_SELECTOR, '.sm-col.col-10.sm-col-6.lg-col-4.px3.mx-auto.mb3') if main_container else None
          
          # print(len(boxes))
          for box in boxes:
               container = box.find_element(By.CSS_SELECTOR, '.white-box.property-list-item.relative')
               link_tag = container.find_elements(By.TAG_NAME, 'a') if container else None
               tag = link_tag[1] if container else None
               link = [tag.get_attribute('href')] if tag else 'Nan'  
               links.append(link)
               
               
          # to scroll the page to bottom
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
          
          try:
               next_container = driver.find_element(By.CSS_SELECTOR, '.inline-block.ml2')
               
               if next_container is None:
                    break
               else:
                    url = next_container.find_element(By.TAG_NAME, 'a')
                    
                    if url is None:
                         break
                    else:
                         url = url.get_attribute('href')
                         print(url)
                         
          except Exception as e:
               break
               
     return links
          
     
     
def main():
     driver = driverInitialialization()
     
     url = 'https://remax-central.com.sv/en'
     
     links = urlExtractor(driver, url)
     
     df = pd.DataFrame(links, columns=['urls'])
     
     df.to_csv('urls.csv', index=False)
     
     

if __name__ == '__main__':
     main()
     
     
     
     

