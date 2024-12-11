import json
import requests
import logging
import requests
import pandas as pd

from datetime import datetime

from base.log_config import dictConfig
logger = logging.getLogger("xyz_storage")




url = "https://dashboard.n49.com/native/filterReviews/null/jhs0krj2kdzgwej4s"

querystring = {"mode":"multi"}

payload = {"LastEvaluatedKey": [
          {
               "_id": "m4fs9cd6t9s86ngo7",
               "dateCreated": 1733202000000,
               "entityId": "jhrtgyf3izoyc0rih"
          },
          {
               "_id": "m4ftavxsirvatynmw",
               "dateCreated": 1732942800000,
               "entityId": "jwjbbu0fdl26ixz0v"
          },
          {
               "_id": "m4ef8vp9qcpmi7t0u",
               "dateCreated": 1733590874493,
               "entityId": "jhrvg39uijr5q9mo3"
          },
          {
               "_id": "m44bv7kjc4i7s3n5p",
               "dateCreated": 1732980536083,
               "entityId": "jhrtqujzw0ystxyfk"
          },
          {
               "_id": "AbFvOqnH2oiAdP-1GAL7cXYDvEmkf3Brs33tNC8vpKMqc_OOOBNAwADXqD0_HI_8i-Y8EmbLkoDxUg",
               "dateCreated": 1733234115769,
               "entityId": "jhrur79akaghyr692"
          }
     ]}
headers = {
     "cookie": "XSRF-TOKEN=eyJpdiI6InYrclV5T3BMbGtpUDd3U0h3Y3ArTEE9PSIsInZhbHVlIjoiSlVsOW02YlE3TFVaRkNOd1RtYzdDRkhxSEJybHFwbjl2UnlsTllPUlFHa2RTbzgxeU41ejhYdjg3dEplSnUwdGE4bVZ3djg5UlV6MjhuYVp1RWR0aHQ0OU1GY1FHMWg4Z2h6VmdmdjZFbVM5Z1FZOUk4dklzUy95UzNMSnlsTysiLCJtYWMiOiJjODY4ZGJiYmMzYTFkNzA5ZDljMjg2OTE4OTA5MjVjYzRlYWIwMWQwYjZmZmU1NmJjOWEwNTE1OGUyMGJkNjQ1IiwidGFnIjoiIn0%253D; storageca_session=eyJpdiI6Im1OamlGRkpOTXh3OHlsUENzaEVGd0E9PSIsInZhbHVlIjoiSU5Xb0VpUEJrN05mQUloSTVlQVFlWjQ3bVplZm03VVNuenNFRUhSVHlmbHdLN1Jpb3ROSDFxeTBXVWhwTktZWFB3OTlaYmE0SEt4QjI0VkJoeWNoMExyWG9xamV0MFNQa0gyOUx5emFmaDN6dkhQYUpQN0VkQ0FyWWYxckgweXIiLCJtYWMiOiIwZmQzZDQ1NDE2MmRjOTE5YzFlNTlkMmQ1OWE2OThjYTE3MjE5MDBiOTNhZDIyOWEzMTcwZTNmN2JhNGY0NDI3IiwidGFnIjoiIn0%253D",
     "accept": "*/*",
     "accept-language": "en-US,en;q=0.8",
     "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjE2NDQzNDY2MzEsInVzZXJfaWQiOiJrdHN4dzlramxkZ3RzZDNqMSIsImV4cCI6MTI5NzY0NDM0NjYzMX0.FZeMMsZlix1eQ1aJFmQ0MV_L_ezFb4RhrqCIhceTT-w",
     "content-type": "application/json",
     "origin": "https://www.xyzstorage.com",
     "priority": "u=1, i",
     "referer": "https://www.xyzstorage.com/",
     "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
     "sec-ch-ua-mobile": "?1",
     "sec-ch-ua-platform": '"Android"',
     "sec-fetch-dest": "empty",
     "sec-fetch-mode": "cors",
     "sec-fetch-site": "cross-site",
     "sec-gpc": "1",
     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

def update_payload_with_last_evaluated_key(api_response):
     last_evaluated_key = api_response.get('LastEvaluatedKey', [])
     if last_evaluated_key:
          payload['LastEvaluatedKey'] = last_evaluated_key
          logger.info(f"Updated payload with LastEvaluatedKey: {last_evaluated_key}")
     else:
          logger.info("No LastEvaluatedKey found in the response.")


def sample_generator(json_data):
     with open("sample.json","w") as file:
          json.dump(json_data, file, indent=4)
          logger.info("Sample file generated")

base_payload = {
     "LastEvaluatedKey": []
}


def format_timestamp(json_date):
     if json_date is not None:
          date = datetime.utcfromtimestamp(json_date / 1000).strftime("%Y-%m-%d %H:%M:%S")
     return date


def all_data_extractor():
     all_reviews = []
     payload = base_payload.copy()  # Start with an empty LastEvaluatedKey

     while True:
          try:
               response = requests.post(url, json=payload, headers=headers, params=querystring)
               logger.info(f"Status Code: {response.status_code}")

               if response.status_code != 200:
                    logger.error("API request failed.")
                    break

               try:
                    json_data = response.json()
               except Exception as e:
                    logger.error(f"something went wrong while changing data in json format", exc_info=e)
                    logger.debug(f"Raw response : {response.text}")
                    break

               # Collect reviews
               reviews_data = json_data.get('reviews', [])
               for item in reviews_data:
                    review = item.get("content", None)
                    json_date = item.get("dateCreated", None)
                    posted_date = format_timestamp(json_date)
                    rating = item.get("rating", None)
                    review_type = item.get("reviewType", None)

                    # User details
                    user_detail = item.get("user", {})
                    email = user_detail.get("email", None)
                    fullname = user_detail.get("fullName", None)
                    name = fullname or user_detail.get("firstName", None)

                    # Location
                    location_obj = item.get("entityInfo", {})
                    location = None
                    if location_obj:
                         location_data = location_obj.get("reviewFeedUrls", {})
                         location = location_data.get("5734f48a0b64d7382829fdf7", None)
                         if location:
                              location = location.split("/")[4] if len(location.split("/")) > 3 else None

                    # Append review data
                    all_reviews.append({
                         "Review": review,
                         "PostedDate": posted_date,
                         "Rating": rating,
                         "ReviewType": review_type,
                         "Email": email,
                         "Name": name,
                         "Location": location
                    })

                    logger.info(f"collected reviews --> {len(all_reviews)}")

               # Update LastEvaluatedKey for pagination
               last_evaluated_key = json_data.get('LastEvaluatedKey', None)
               if last_evaluated_key:
                    payload["LastEvaluatedKey"] = last_evaluated_key
                    logger.info(f"Fetching next batch with LastEvaluatedKey: {last_evaluated_key}")
                    logger.info("")
               else:
                    logger.info("No more pages to fetch.")
                    break

          except ValueError as e:
               logger.error("Failed to parse response as JSON", exc_info=e)
               break
          except Exception as e:
               logger.error("Failed to make API request", exc_info=e)
               break


     # Create DataFrame from collected data
     reviews_df = pd.DataFrame(all_reviews)
     logger.info(f"Collected {len(all_reviews)} reviews.")

     return reviews_df


def main():
     df = all_data_extractor()
     
     if not df.empty:
          df.to_csv("details.csv", index=False)
          logger.info("Scraping Completed")
     else:
          logger.error("Something went wrong.Empty csv file is generated")


if __name__ == "__main__":
     main()
