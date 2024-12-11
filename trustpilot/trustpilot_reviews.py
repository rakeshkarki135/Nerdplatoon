import requests
import logging

from bs4 import BeautifulSoup

from base.log_config import dictConfig
logger = logging.getLogger("trustpilot")


def soup_creator(url):
    response = requests.get(url)

    if response.status_code != 200:
        logger.error("Failed to get url ---> {url} , status-code ---> {response.status_code}")
        return 
    
    html_content = response.content
    soup = BeautifulSoup(html_content, "lxml")

    if soup is None:
        logger.error("soup is not found")
        return


    container = soup.find("div", class_ = "styles_mainContent__nFxAv")
    if container is not None:
        # logger.info(container)
        return container
        

def main_review_extractor(soup):
    try:
        main_container = soup.find("section", class_ = "styles_reviewsContainer__3_GQw")

        if main_container is not None:
            content_boxes = main_container.find_all("div", class_ = "styles_reviewCardInner__EwDq2")
            logger.info(len(content_boxes))

            # for box in content_boxes:




        

    except Exception as e:
        logger.error("something went wrong while getting main container", exc_info=e)



def multiple_url_runner():
    pass

def main():
    url = "https://www.trustpilot.com/review/accessstorage.ca"
    
    soup = soup_creator(url)

    main_review_extractor(soup)


if __name__ == "__main__":
    main()