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
        logger.error(f"Cannot create the soup at link ---> {url}, statud_code --->{response.status_code}")
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
        logger.error("somehing went wrong while geting description", exc_info=e)



def detail_scraper(soup):

    try:
        review_boxes = soup.find_all("div", class_ = "lg:tw-grid lg:tw-grid-cols-4 lg:tw-gap-x-gutter--desktop")
        
        for box in review_boxes:
            rating_and_desc_container = box.find("div", class_ = "tw-order-1 lg:tw-order-2 lg:tw-col-span-3 tw-overflow-x-auto")

            if rating_and_desc_container is not None:
                rating = rating_scraper(rating_and_desc_container)
                print(rating)
        
                update_date = update_date_scraper(rating_and_desc_container)
                print(update_date)

                description = description_scraper(rating_and_desc_container)
                print(description)

            detail_container = box.find("div", class_ = "tw-mb-xs md:tw-mb-sm")

            break





    except Exception as e:
        logger.error(f"could not scrape the details")


def main():
    url = "https://apps.shopify.com/google-reviews-trust-badge/reviews?search_id=e71d14c6-b497-4b5b-843c-918c19b9d815"

    soup = soup_creator(url)
    
    detail_scraper(soup)



if __name__ == "__main__":
    main()