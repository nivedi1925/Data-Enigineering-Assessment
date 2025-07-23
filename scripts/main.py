
import pandas as pd
import argparse
from load.load import load_lookup_tables,load_leads,load_hoa_details,\
            load_property_details,load_property_address,\
            load_property_rehab,load_property_valuation,load_tax_details

from transform.transform import tranform_df,transform_df_HOA,\
                    tranform_df_Valuation,transform_df_Rehab

from extract.extract import extract_json
from sqlalchemy import create_engine
from config.config import USER_NAME,PASSWORD,HOST,PORT,DB_NAME,LOG_TO_CONSOLE
from utils.logger import setup_logger
import sys


db_url = "mysql+pymysql://" + USER_NAME + ":" + PASSWORD + "@" + HOST + ":" + PORT + "/" + DB_NAME
logger = setup_logger('main', to_console=LOG_TO_CONSOLE)





def main():
    logger.info("ETL job started...!")
    # get file path as command line argument 
    parser = argparse.ArgumentParser(description="ETL Script")
    parser.add_argument("filename", help="Path to the input JSON file")
    args = parser.parse_args()
  
    # extract json file into different dataframes according to the structure 
    try:
        print("Extracting json file ....")
        logger.info(f"Attempting to read JSON file: {args.filename}")
        df, df_HOA, df_Rehab, df_Valuation = extract_json(args.filename)
        logger.info("JSON extraction completed.")

    except Exception as e:
        logger.error("Extraction failed!")
        print("\n"+ "  "*10+"ETL task terminated. Please follow the log file for details."+"  "*10+"\n")
        sys.exit(1)

    # transformations on dataframes
    try:
        print("Transforming the data ....")
        logger.info("Dataframe transformation started.")

        df = tranform_df(df)
        logger.info("Properties Dataframe transformation compleated.")
        
        df_HOA = transform_df_HOA(df_HOA)
        logger.info("HOA Dataframe transformation compleated.")
       
        df_Rehab = transform_df_Rehab(df_Rehab)
        logger.info("Rehab Dataframe transformation compleated.")
      
        df_Valuation = tranform_df_Valuation(df_Valuation)
        logger.info("Valuation Dataframe transformation compleated.")

        
    
    except Exception as e:
        logger.error("Transformation failed!")
        print("\n"+ "  "*10+"ETL task terminated. Please follow the log file for details."+"  "*10+"\n")
        sys.exit(1)


    # create database connection instance 
    engine = create_engine(db_url)

    try:
        print("Loading the data to tables...")

        logger.info("Loading the data to MySQL database.")
        #load all the tables one by one
        lookup_ids = load_lookup_tables(df,engine)
        

        load_property_details(df,lookup_ids,engine)
        logger.info("Table load_property_details compleate.")

        load_property_address(df,lookup_ids,engine)
        logger.info("Table load_property_address compleate.")

        load_tax_details(df,engine)
        logger.info("Table load_tax_details compleate.")

        load_leads(df,lookup_ids,engine)
        logger.info("Table load_leads compleate.")

        load_property_valuation(df_Valuation,engine)
        logger.info("Table load_property_valuation compleate.")

        load_hoa_details(df_HOA,engine)
        logger.info("Table load_hoa_details compleate.")

        load_property_rehab(df_Rehab,engine)
        logger.info("Table load_property_rehab compleated.")

        logger.info("ETL Successful.")
        print("\n"+ "  "*10+"ETL task compleated. Please follow the log file for details."+"  "*10+"\n")

    except Exception as e:
        logger.error("Database Load failed!")
        print("\n"+ "  "*10+"ETL task terminated. Please follow the log file for details."+"  "*10+"\n")
        sys.exit(1)


if __name__ == "__main__":
    main()