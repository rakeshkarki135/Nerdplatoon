import json
import requests
import logging
from logging import getLogger

from base.log_config import dictConfig
logger = getLogger("reviews")

url = "https://www.amazon.com/hz/reviews-render/ajax/medley-filtered-reviews/get/ref=cm_cr_dp_d_fltrs_srt"

payload = "language=en_US&asin=B0BQD58D96&sortBy=recent&scope=reviewsAjax1"
headers = {
    "cookie": 'session-id=144-8358806-6356635; i18n-prefs=USD; sp-cdn="L5Z9:NP"; skin=noskin; ubid-main=134-5372070-6509469; lc-main=en_US; id_pkel=n0; id_pk=eyJuIjoiMCJ9; session-token=+uD9n5wQC8dZotr0UACsg1tA93+QrERZFSsA1lHfOXSgd0zU84++gxjMf62+6FyuI9Wi/QUSEKVAf5Vl3r3LFuhHLeD8ylERt3dojqr7Es9d4h0kWPWVrzi1yx3dgg+CAjhhlZZYLTVPgLFUAquIYDxK9TQv/byrSyvKjnFUqC8QzuJMKcP2wwwvfd3SytQ5YT2FaH6ENhzYgvU6va/x2Q9y4fTTxY/AfDhK35JKKbY194b3qhNrZZsfQg7SGlzX9QTXBhMTDSR7hq78zQRU3Y/ZsAlZ8gisJ7DqdOGWVf5ZMcntTqOXiuzKacZ84sC+mhJcSpDApDoPFQN4vcs54oVDkNl0rdLW; JSESSIONID=E67A76D28A75CEAF6A90A873DC1AF7D7; session-id-time=2082787201l; csm-hit=tb:TADSX1E9VNSD7ZSYB8RV+b-P3994EE37DB4P4MA4GDJ|1735291795014&t:1735291795014&adb:adblk_yes',
    "accept": "text/html,*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "device-memory": "8",
    "downlink": "14",
    "dpr": "2",
    "ect": "4g",
    "origin": "https://www.amazon.com",
    "priority": "u=1, i",
    "referer": "https://www.amazon.com/ASUS-TUF-Intel%C2%AE12th-Motherboard-Thunderbolt/dp/B0BQD58D96?_encoding=UTF8&content-id=amzn1.sym.860dbf94-9f09-4ada-8615-32eb5ada253a&dib=eyJ2IjoiMSJ9.QkpDjjxjIABcw7jorE25B-ERcGxDfut5cIBx9LTDWRF-e-t6nqxY0z5wlZ8KGA9PbLz5zUhkNy2mKdDj-HiL4Ss-W-JOJ1eIxOuldrlD5o29E0C2KKxliPMQO5q9KWflRxob-OF6WFTS7B5aLzWM02MAuHGjokohfhQsVNfbcsjA73j_dIAIfbSW4esMXqYCj8sz98RbqAEbXrSFpD57xsi_nyq90Knj8xNQDzK-jvZVCdphHy67n6QrtY76J6DNMUnkbkIqowRFQWU4pPADv2DFcWGxqPBzmnRKBCfha5uCKZ900JzJF0H7MOj4C3cEazOUWbz-Ij1KxMwHiDz7NH5i4N1rtMflSDSn7VVwRs11q_2mezDMYORTkvlRENAA_FC1oZObbxLj1DVqhNHD5eq2dfTpPyu-hm-uUaPYdfGqup56TqGlyFmFd9B277pf.p7fs4-vhwyCAB3JFse-De-x8TzyswJIBqKdCszHaH4U&dib_tag=se&keywords=gaming&pd_rd_r=1117ead0-040e-4e40-b1a6-c34eac602718&pd_rd_w=pGPRw&pd_rd_wg=nKLV6&pf_rd_p=860dbf94-9f09-4ada-8615-32eb5ada253a&pf_rd_r=TADSX1E9VNSD7ZSYB8RV&qid=1735288736&sr=8-21&th=1",
    "rtt": "250",
    "sec-ch-device-memory": "8",
    "sec-ch-dpr": "1",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-ch-viewport-width": "1033",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "viewport-width": "1033",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.request("POST", url, data=payload, headers=headers)

try:
    json_data = response.json()
    
    with open("sample.json","w") as file:
        json.dump(json_data, file)
        logger.info("sample is generated")
        
except Exception as e:
    logger.error("something went wrong", exc_info=e)