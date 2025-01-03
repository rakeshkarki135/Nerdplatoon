import pandas as pd

df1 = pd.read_csv("xml_links.csv")

df2 = pd.read_csv("xml5_links.csv")

df = pd.concat([df1, df2], ignore_index=True)

cleaned_df = df.drop_duplicates(subset="url", keep="first")

cleaned_df.to_csv("merged_urls.csv", index=False)