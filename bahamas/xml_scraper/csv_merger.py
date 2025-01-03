import pandas as pd
import logging

from base.log_config import dictConfig
logger = logging.getLogger("merger")

    
def csv_merger(file_paths: list[str], output_file: str = "merged_urls_Demo.csv"):
    merged_df = pd.DataFrame()
    for file in file_paths:
        try:
            df = pd.read_csv(file)
            merged_df = pd.concat([df, merged_df], ignore_index=False)  
            
        except Exception as e:
            logger.error(f"Failed to merge CSV files, Error at --> {file}", exc_info=e)
    
    if "url" in merged_df.columns:
        cleaned_df = merged_df.drop_duplicates(subset="url", keep="first")
    else:
        logger.info("No duplicate links found")
        cleaned_df = merged_df
        
    cleaned_df.to_csv(f"./csv/{output_file}", index=False)
    logger.info("Merging CSV file is Comleted")
    
    
def main():
    file_paths = ["./csv/xml_links.csv","./csv/xml5_links.csv","./csv/xml6_links.csv"]
    
    csv_merger(file_paths)
    
    
if __name__ == "__main__":
    main()
    
    
    