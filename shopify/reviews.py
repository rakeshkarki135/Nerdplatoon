import requests 
import logging
import pandas as pd
import time

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver

from base import log_config
logger = logging.getLogger("reviews")

def driver_initialization():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)
    return driver


def soup_creator(url):
    driver = driver_initialization()
    driver.get(url)

    time.sleep(3)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    section = soup.find("section", id="arp-reviews")

    if section is not None:
        return section
        # container = section.find("div", class_ = "tw-col-span-full md:tw-col-span-9 lg:tw-col-span-8 lg:tw-pl-gutter--desktop")

    
def rating_scraper(soup):
    try:
        rating_element = soup.find("div", class_ = "tw-flex tw-relative tw-space-x-0.5 tw-w-[88px] tw-h-md")
        if rating_element:
            rating_txt = rating_element.get('aria-label')
            rating_txt = rating_txt.split()

            if len(rating_txt) > 0:
                rating = rating_txt[0]
                
        return rating
    except Exception as e:
        logger.error("something went wrong while getting ratings", exc_info=e)


def update_date_scraper(soup):
    try:
        update_date_element = soup.find("div", class_ = "tw-text-body-xs tw-text-fg-tertiary")

        if update_date_element is not None:
            update_date = update_date_element.text.strip()
            
        return update_date
    except Exception as e:
        logger.error("something went wrong while getting update date")


def description_scraper(soup):
    try:
        description_element = soup.find("div", class_ = "tw-mb-xs md:tw-mb-sm")
        if description_element is not None:
            description = description_element.text.strip()
            
        return description
    except Exception as e:
        logger.error("something went wrong while getting description", exc_info=e)


def store_detail_scraper(soup):
    title, location, span = None, None, None 

    try:
        title_element = soup.find("div", class_ = "tw-text-heading-xs tw-text-fg-primary tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap")
        
        if title_element is not None:
            title = title_element.text.strip()
            
            location_element = title_element.find_next_sibling()
            if location_element is not None:
                location = location_element.text.strip()
                
                span_element = location_element.find_next_sibling()
                if span_element is not None:
                    span = span_element.text.strip()
                    
        return title, location, span         
    except Exception as e:
        logger.error("something went wrong while getting store details", exc_info=e)


def main_detail_scraper(soup):
    try:
        review_list = []
        review_boxes = soup.find_all("div", class_ = "lg:tw-grid lg:tw-grid-cols-4 lg:tw-gap-x-gutter--desktop")
    
        for box in review_boxes:
            rating_and_desc_container = box.find("div", class_ = "tw-order-1 lg:tw-order-2 lg:tw-col-span-3 tw-overflow-x-auto")

            if rating_and_desc_container is not None:
                rating = rating_scraper(rating_and_desc_container)
                update_date = update_date_scraper(rating_and_desc_container)
                description = description_scraper(rating_and_desc_container)

            details_container = box.find("div", class_ = "tw-order-2")
            
            if details_container is not None:
                store_title, location, span = store_detail_scraper(details_container)
            
            review_list.append({
                "store_name" : store_title,
                "location" : location,
                "span" : span,
                "ratings" : rating,
                "posted_date" : update_date,
                "review" : description
            })
        
        return review_list
    except Exception as e:
        logger.error(f"something went wrong while getting the details")


def next_page_link_scraper(soup):
    url = None
    try:
        main_container = soup.find("div", class_ = "tw-flex tw-justify-center tw-py-2xl")
        # logger.info(main_container)
        
        if main_container is not None:
            pagination_container = main_container.find("div", {"aria-label":"pagination"})
        
            if pagination_container is not None:
                next_page_element = pagination_container.find("a", {"rel":"next"})
                
                if next_page_element is not None:
                    url = next_page_element.get("href")
                    logger.info(url)
            else:
                logger.info("pagination continer not found")
                    
        else:
            logger.info("main container not found")
            
        return url   
    except Exception as e:
        logger.error("something went wrong while getting next page", exc_info=e)


def main():
    url = "https://apps.shopify.com/google-reviews-trust-badge/reviews?search_id=e71d14c6-b497-4b5b-843c-918c19b9d815"
    all_reviews = []

    while True:
        try:
            soup = soup_creator(url)
            if not soup:
                logger.info("soup is not found")
                return
            
            reviews = main_detail_scraper(soup)

            if not reviews:
                logger.info("review lis is empty")
                return 
            all_reviews.extend(reviews)
            
            logger.info(f"link succefully processed  ---> {url}")
            
            url = next_page_link_scraper(soup)
            if not url:
                logger.info("No more pages to process. Ending loop.")
                break

            logger.info(f"Proceeding to next page: {url}")
            
        except Exception as e:
            logger.info("something went wrong in while loop", exc_info=e)


    df = pd.DataFrame(all_reviews)
    df.to_csv("review.csv", index=False)

    logger.info("CSV file is generated")
    

if __name__ == "__main__":
    main()