import pandas as pd
from bs4 import BeautifulSoup

# Open and read the XML file (sitemap.xml)
with open('sitemap_4.xml', 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Parse the XML content using BeautifulSoup
soup = BeautifulSoup(xml_content, 'xml')


# Extract the text content (URLs) from the <loc> tags
urls = []
url_elements = soup.find_all("xhtml:link", {"hreflang":"en"})
for url_element in url_elements:
        url = url_element.get("href")
        urls.append(url)
        
    
    

# Create a Pandas DataFrame with the URLs
df = pd.DataFrame(urls, columns=['url'])

df = df.drop_duplicates(subset=['url'], keep='first')

# Save the DataFrame to a CSV file
df.to_csv('xml_links.csv', index=False)

