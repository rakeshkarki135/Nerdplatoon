import json
import requests
import logging

from base.log_config import dictConfig
logger = logging.getLogger("xyz_storage")


import requests

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


try:
     response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
     logger.info(f"Status Code: {response.status_code}")
     logger.info(f"Response Text: {response.text}")

     try:
          json_data = response.json()
          # Extract specific parts (e.g., form fields)
          reviews = json_data.get('reviews')
               
          # Save extracted fields to a file
          with open('sample.json', 'w') as file:
               json.dump(reviews, file, indent=4)
               logger.info("Extracted fields saved to extracted_fields.json")
     except ValueError as e:
          logger.error("Failed to parse response as JSON", exc_info=e)

except Exception as e:
     logger.error("Failed to make api request", exc_info=e)
