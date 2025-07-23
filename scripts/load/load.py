import pandas as pd
from utils.logger import setup_logger
import sys
logger = setup_logger('load')



def load_lookup_tables(df,engine):

    lookup_tables = {
    "layout_lookup" : "layout",
    "market_lookup": "market",
    "property_type_lookup":"property_type",
    "subdivision_lookup":"subdivision",
    "flood_zone_lookup" : "flood",
    "parking_type_lookup": "parking",
    "reviewed_status_lookup":"reviewed_status",
    "most_recent_status_lookup":"most_recent_status",
    "source_lookup":"source",
    "selling_reason_lookup":"selling_reason",
    "final_reviewer_lookup":"reviewer_name"
    }
    
    try:
        for table_name,column_name in lookup_tables.items():
            pd.DataFrame(df[column_name].dropna().unique(),columns=[column_name]).to_sql(
            name= table_name,        # table name
            con=engine,
            if_exists='append',          # or 'replace' or 'fail'
            index=False       )         # don't write DataFrame index as column
    except Exception as e:
        logger.error("Failed to store lookup tables!")   
    



    ### Read the lookup table and get ids so that update in prperty table.

    lookup_ids = {}
    try:
        for table_name,column_name in lookup_tables.items():
            lookup = pd.read_sql_table(table_name, engine)
            data_dict = lookup.to_dict(orient='tight')
            items = data_dict['data']
            sub_dictionary = {}
            for item in items:
                sub_dictionary[item[1]] = item[0]
            lookup_ids[table_name] = sub_dictionary
    except Exception as e:
        logger.error("Failed to load lookup tables!") 


    return lookup_ids


def load_property_details(df,lookup_ids,engine):

    df['parking_type_id'] = df['parking'].apply(lambda x: lookup_ids["parking_type_lookup"].get(x, pd.NA))
    df['layout_id'] = df['layout'].apply(lambda x: lookup_ids["layout_lookup"].get(x, pd.NA))
    df['flood_id'] = df['flood'].apply(lambda x: lookup_ids["flood_zone_lookup"].get(x, pd.NA))
    df['market_id'] = df['market'].apply(lambda x: lookup_ids["market_lookup"].get(x, pd.NA))
    df['property_type_id'] = df['property_type'].apply(lambda x: lookup_ids["property_type_lookup"].get(x, pd.NA))

    # Select specific columns
    subset_df = df[['property_title',
        'highway',
        'train', 
       'sqft_basement', 
       'htw', 
       'pool', 
       'commercial',
        'water', 
        'sewage',
       'year_built',
        'sqft_mu', 
        'sqft_total', 
        'bed',
        'bath',
       'basement', 
       'rent_restricted',
       'neighborhood_rating', 
       'school_average', 
       'property_id',
       'parking_type_id', 
       'layout_id', 
       'flood_id',
        'market_id',
       'property_type_id']]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='property_details',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.error("Failed to load_property_details tables!") 

def load_property_address(df,lookup_ids,engine):

    df['subdivision_id'] = df['subdivision'].apply(lambda x: lookup_ids["subdivision_lookup"].get(x, pd.NA))
    subset_df = df[['address',
                    'property_id',
                'city',
                'latitude',
                'longitude',
                'state',
                'street_address',
                'subdivision_id',
                'zip']]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='property_address',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.error("Failed to load_property_address tables!") 

def load_tax_details(df,engine):
    subset_df = df[['property_id',
                    'tax_rate',
                    'taxes']]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='tax_details',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.exception("Failed to load_tax_details tables!") 

def load_leads(df,lookup_ids,engine):
    df['reviewed_status_id'] = df['reviewed_status'].apply(lambda x: lookup_ids["reviewed_status_lookup"].get(x, pd.NA))
    df['most_recent_status_id'] = df['most_recent_status'].apply(lambda x: lookup_ids["most_recent_status_lookup"].get(x, pd.NA))
    df['source_id'] = df['source'].apply(lambda x: lookup_ids["source_lookup"].get(x, pd.NA))
    df['selling_reason_id'] = df['selling_reason'].apply(lambda x: lookup_ids["selling_reason_lookup"].get(x, pd.NA))
    df['final_reviewer_id'] = df['reviewer_name'].apply(lambda x: lookup_ids["final_reviewer_lookup"].get(x, pd.NA))

    subset_df = df[['property_id',
                    'reviewed_status_id',
                    'most_recent_status_id',
                    'source_id',
                    'selling_reason_id',
                    'final_reviewer_id',
                    'seller_retained_broker',
                    'occupancy',
                    'net_yield',
                    'irr'
                    ]]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='leads',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.error("Failed to load_leads tables!") 


def load_property_rehab(df_Rehab,engine):
    subset_df = df_Rehab[['property_id',
                    'underwriting_rehab',
                    "rehab_calculation",
                    'paint',
                    'flooring_flag',
                    'foundation_flag',
                    'roof_flag',
                    'hvac_flag',
                    'kitchen_flag',
                    'bathroom_flag',
                    'appliances_flag',
                    'windows_flag',
                    'landscaping_flag',
                    'trashout_flag',
                    ]]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='property_rehab',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.exception("Failed to load_property_rehab tables!") 

def load_hoa_details(df_HOA,engine):
    subset_df = df_HOA[['property_id',
                    'hoa',
                    'hoa_flag']]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='hoa_details',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.error("Failed to load_hoa_details tables!") 

def load_property_valuation(df_Valuation,engine):
    subset_df = df_Valuation[['property_id',
                    'list_price',
                    'previous_rent',
                    'arv',
                    'rent_zestimate',
                    'low_fmr',
                    'redfin_value',
                    'zestimate',
                    'expected_rent',
                    'high_fmr',
                    ]]
    try:
        # Write to SQL
        subset_df.to_sql(
            name='property_valuation',
            con=engine,
            if_exists='append',  # or 'replace' or 'fail'
            index=False
        )

    except Exception as e:
        logger.error("Failed to load_property_valuation tables!") 
