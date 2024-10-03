from bs4 import BeautifulSoup
import requests    
import pandas as pd          


def get_soup(url):
     r = requests.get(url)
     return BeautifulSoup(r.text, 'lxml')

def detail_extraction():
     df = pd.read_csv('business_data.csv')
     
     # print(obj)
     main_df = pd.DataFrame({'Title':df['Title'],'Link':df['Link'],'Address':df['Address'],'Last_updated_Date':['']*len(df),'Category':['']*len(df),'Description':['']*len(df),'Phone':['']*len(df),'Email':['']*len(df),'Website':['']*len(df)})
     
     # print(new_df)
     for i,link in enumerate(df['Link']):
          # print(link)
          print(i,link)
          soup = get_soup(link)
     
          container = soup.find('div', class_='tab-content')
          last_updated = container.find('div', class_='updated-date float-left') if container else None
          last_updated = last_updated.text.strip() if last_updated else 'Nan'
          # print(last_updated)
          cat_box = container.find('div', class_='description mb-5 pt-3') if container else None
          category = cat_box.find('a') if cat_box else None
          category = category.text.strip() if category else 'Nan'
          description = cat_box.find('p', {'itemprop':'description'}) if cat_box else None
          description = description.text.strip() if description else 'Nan'
          # print(description)
          contact_container = container.find('div', id='contact') if container else None
          phone = contact_container.find('p').find('meta',{'itemprop':'telephone'}) if contact_container else None
          email = contact_container.find('meta',{'itemprop':'email'}) if contact_container else None
          website = contact_container.find_all('p')[-1].find('a') if contact_container else None
          
          if email:
               email = email['content']
          else:
               email = 'Nan'
               
          
          if phone:
               phone = phone['content']
          else:
               phone = 'Nan'
               
               
          if website is None:
               website = 'Nan'
          else:
               website = website.get('href')
               
          # print(website,phone,email,description,last_updated)
          # break
          main_df.at[i, 'Last_updated_Date'] = last_updated
          main_df.at[i, 'Category'] = category
          main_df.at[i, 'Description'] = description
          main_df.at[i, 'Phone'] = phone
          main_df.at[i, 'Email'] = email 
          main_df.at[i, 'Website'] = website
          
          # print(main_df)
          # break
          # # if i > 5:
          # #      print(main_df)
          # # else:
          # #      break
     
     main_df['Last_updated_Date'] = main_df['Last_updated_Date'].str.replace(r'[LastUpdated:\n\s]','',regex=True)
     main_df.to_csv('business_detail.csv')

     

def main():
     detail_extraction()


if __name__ == "__main__":
     main()





     
     
     