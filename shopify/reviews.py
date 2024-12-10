import requests 
import logging
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime

from base import log_config
logger = logging.getLogger("reviews")


def soup_creator(url):
    response = requests.get(url, timeout=6)
    html_content = response.content
    if response.status_code != 200:
        logger.error(f"Cannot create the soup at link ---> {url}, status_code --->{response.status_code}")
        return

    soup = BeautifulSoup(html_content, 'lxml')
    
    section = soup.find("section", id="arp-reviews")

    if section is not None:
        container = section.find("div", class_ = "tw-col-span-full md:tw-col-span-9 lg:tw-col-span-8 lg:tw-pl-gutter--desktop")

        if container is not None:
            return container


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
    try:
        # main_container = soup.find("div", class_ = "tw-flex tw-justify-center tw-py-2xl")
        # logger.info(main_container)
        
        # if main_container is not None:
        # pagination_container = soup.find("div", class_ = "tw-flex tw-items-center")
        # logger.info(pagination_container)
        
        # if pagination_container is not None:
        next_page_element = soup.find("a", {"rel":"next"})
        logger.info(next_page_element)
        
        if next_page_element is not None:
            url = next_page_element.get("href")
        else:
            url = None
            
        logger.info(url)
    # else:
        #     logger.info("pagination continer not found")
                
        # else:
        #     logger.info("main container not found")
            
        return url   
    except Exception as e:
        logger.error("something went wrong while getting next page", exc_info=e)
    

def main():
    url = "https://apps.shopify.com/google-reviews-trust-badge/reviews?search_id=e71d14c6-b497-4b5b-843c-918c19b9d815"
    
    all_reviews = []
    while True:
        try:
            soup = soup_creator(url)
            reviews = main_detail_scraper(soup)
            all_reviews.extend(reviews)
            
            logger.info(f"link succefully processed  ---> {url}")
            
            url = next_page_link_scraper(soup)
            
            if url is None:
                break
            
        except Exception as e:
            logger.info("while loop is terminated, all reviews extracted", exc_info=e)
    
    df = pd.DataFrame(all_reviews)
    df.to_csv("review.csv", index=False)
    
            

if __name__ == "__main__":
    main()