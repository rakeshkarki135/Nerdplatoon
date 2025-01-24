import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait


def driver_initialization():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def review_scraper(url, driver):
    driver.get(url)
    time.sleep(5)
    try:
        main_container = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Camion jo pizza']")))
        if main_container:
            button = main_container.find_element(By.CLASS_NAME, "IAbLGd")
            if button:
                # driver.execute_script("arguments[0].scrollIntoView(true);", button)
            
            # Wait for the button to be clickable
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(button))
                button.click()
                time.sleep(5)
        else:
            print("button is not found")
            return 
            
    except Exception as e:
        print(f"Error occured while getting main container --> {e}")
        return 
        
    try:
        container =  driver.find_element(By.ID, "fDahXd")
        if container:
            new_button = container.find_element(By.XPATH, "//div[@class='fxNQSd'][@data-index='1']")
            if new_button:
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(newest_button))
                new_button.click()
                time.sleep(5)
                # newest_button = new_buttons[1]
                
                # newest_button.click()
    except Exception as e:
        print(f"Error oocured while getting newest button container ---> {e}")
        
    try:
        username_element = main_container.find_element(By.CLASS_NAME, "d4r55")
        if username_element:
            username = username_element.text.strip()
            return username
            
        else:
            print("Username is not found")
    except Exception as e:
        print(f"Error ocured while getting review container --> {e}")



def main():
    url = "https://maps.app.goo.gl/25oQjrYjg1eFcuUu6"
    
    driver = driver_initialization()
    username = review_scraper(url, driver)
    
    df = pd.DataFrame([{"username":username}])
    df.to_csv("latest_reviewer.csv",index=False)
    print("Extracted latest Reviewer Detail")
    

if __name__ == "__main__":
    main()