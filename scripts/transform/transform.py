import pandas as pd
from transform.columnsname import *






def tranform_df(df):
    """ Columns and data tranformations
    Parameter:
            df : Pandas dataframe object
    Return:
        Pandas dataframe object
    """

    df["Reviewed_Status"] = df["Reviewed_Status"].str.strip() \
        .str.title() \
            .replace({' ' : None,'Null': None,'Neww' : "New",'' : None})
    

    df["Most_Recent_Status"] = df["Most_Recent_Status"].str.strip() \
                                        .str.title() \
                                            .replace({' ' : None,'' : None,'Null': None,'Close' : "Closed","Cancel":"Cancelled"})
    
    df["Source"] = df["Source"].str.strip() \
        .str.title() \
            .replace({' ' : None,'' : None,'Null': None,'M.L.S.' : "M.L.S","M L S":"M.L.S","Mls":"M.L.S"})
    
    df["Market"] = df["Market"].str.strip() \
        .str.title() \
            .replace({' ' : None,'' : None,'Null': None,"Chicgo":"Chicago","Dalas":"Dallas"})
    
    df["Property_Type"] = df["Property_Type"].str.strip() \
        .str.title() \
            .replace({"Sfr" : "Single Family Home" })
    
    string_value_columns = ["Flood", "Train", "Water", "Sewage", "Parking", "Layout", "Selling_Reason", "Final_Reviewer"]

    for column_name in string_value_columns:
        df[column_name] = df[column_name].str.strip() \
        .str.title()
    
    # common transformation for columns which can be assigned boolean values so that it saves space.
    boolean_dtype_columns = ["Seller_Retained_Broker", "Rent_Restricted", 
                             "BasementYesNo","Commercial","Pool", "HTW", "Occupancy"]

    for column_name in boolean_dtype_columns:
        df[column_name] = df[column_name].str.strip() \
        .str.title() \
            .replace({"No":False,'Yes':True})
        df[column_name] = pd.Series(df[column_name], dtype= 'boolean')


    df.rename(columns=property_columns_rename, inplace = True)
    return df

def transform_df_HOA(df_HOA):
    df_HOA["HOA_Flag"] = df_HOA["HOA_Flag"].str.strip() \
        .str.title() \
            .replace({"No":False,'Yes':True})
    df_HOA["HOA_Flag"] = pd.Series(df_HOA["HOA_Flag"], dtype= 'boolean')
    df_HOA.rename(columns=hoa_columns_rename, inplace = True)
    return df_HOA


def transform_df_Rehab(df_Rehab):
    rehab_colums = [ "Paint",
        "Flooring_Flag",
        "Foundation_Flag",
        "Roof_Flag",
        "HVAC_Flag",
        "Kitchen_Flag",
        "Bathroom_Flag",
        "Appliances_Flag",
        "Windows_Flag",
        "Landscaping_Flag",
        "Trashout_Flag"]
    
    for column in rehab_colums:
        df_Rehab[column] = df_Rehab[column].replace({"No":False,'Yes':True})
        df_Rehab[column] = pd.Series(df_Rehab[column], dtype= 'boolean')
    
    df_Rehab.rename(columns=rehab_columns_rename, inplace = True)
    return df_Rehab

def tranform_df_Valuation(df_Valuation):
    df_Valuation.rename(columns=valuation_columns_rename, inplace = True)

    return df_Valuation

