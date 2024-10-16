import numpy as np
import pandas as pd

def strip_replace_ws (df):
    df.columns = df.columns.str.lower().str.replace(" ","_")
    return df

def rename_columns (df, column_replacements):
    df.rename(columns=column_replacements, inplace=True)
    return df

def replace_values(df, whole_replacements, substring_replacements):
    """
    df: pandas DataFrame
    replacements_dict: A dictionary where the keys are tuples of values to be replaced,
                       and the values are the new values they should be replaced with.
    """
    for key, value in whole_replacements.items():
        df.replace(key, value, inplace=True)

    for key, value in substring_replacements.items():
        if isinstance(key, str):
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].str.replace(key, value, regex=True)
    return df

    # Update the DataFrame with the results of the apply
    for col in df.columns:
        df[col] = df[col].astype('object')
    
    return df

def get_char(df, *column_names):
    for column_name in column_names:
        if column_name in df.columns:

            def get_complaints(value):
                if isinstance(value, str):
                    split_list = value.split("/")
                    return split_list[1]
                else:
                    return value

            df[column_name] = df[column_name].apply(get_complaints)
            return df

        else:
            raise KeyError(f"Column '{column_name}' not found in the DataFrame")
            
def recast(df, *column_names):
    for column_name in column_names:
        if column_name in df.columns:

            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
            df[column_name] = df[column_name].round(0).astype('Int64')
        else:
            raise KeyError(f"Column '{column_name}' not found in the DataFrame")

    return df

def drop_na (df):
    """
    drops all rows where every value is a null-value
    """
    df.dropna(how = "all", inplace = True)
    return df

def fill_na_mean (df, *column_names):
    """
    Fills null-values in the specified columns with the integer value of the mean of the column.
    """
    for column_name in column_names:
            col_mean = int(df[column_name].mean())
            df[column_name] = df[column_name].fillna(col_mean)  
    return df

def fill_na_gender_ratio (df, *column_names):
    """
    Fills null values in the specified columns with 'M' and 'F'
    based on the ratio of existing values in the column.
    """

    for column_name in column_names:
        nan_indices = df[column_name][df[column_name].isna()].index
        nan_count = len(nan_indices)

        total_count = (df[column_name] == "M").sum() + (df[column_name] == "F").sum()
    
        m_ratio = (df[column_name] == "M").sum()/total_count
        f_ratio = (df[column_name] == "F").sum()/total_count

        nan_m = int(m_ratio*nan_count)
        nan_f = nan_count - nan_m

        fill_values = ['M'] * nan_m + ['F'] * nan_f
        np.random.shuffle(fill_values)
        
        fill_series = pd.Series(fill_values, index=nan_indices)
        
        df[column_name] = df[column_name].fillna(fill_series)
    
    return df

def drop_duplicates(df, *column_names, keep='first'):
    """
    Drops duplicate rows from the DataFrame based on specified columns.
    """
    
    df = df.drop_duplicates(subset=column_names, keep=keep)
    
    return df


def clean_dataset(df, column_replacements, whole_replacements, substring_replacements, char_columns, recast_columns, mean_columns, gender_columns, dupe_columns):
    """
    Main function to clean the dataset by calling a series of cleaning functions in order.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to clean.
    column_replacements (dict): Dictionary for renaming columns.
    whole_replacements (dict): Dictionary for whole value replacements.
    substring_replacements (dict): Dictionary for substring replacements.
    char_columns (list): Column names from which to extract characters.
    recast_columns(list): List of columns to be recast.
    mean_columns (list): List of columns for filling NaN with mean.
    gender_columns (list): List of columns for filling NaN based on gender ratio.
    dup_columns (list): List of columns to check for duplicates.
    
    Returns:
    pd.DataFrame: Cleaned DataFrame.
    """
    
    # Step 1: Strip and replace whitespace in column names
    df = strip_replace_ws(df)
    
    # Step 2: Rename columns based on provided replacements
    df = rename_columns(df, column_replacements)
    
    # Step 3: Replace values based on the dictionaries provided
    df = replace_values(df, whole_replacements, substring_replacements)
    
    # Step 4: Get specific character from a column (example column, adjust as needed)
    df = get_char(df, *char_columns)

    # Step 5: Recast specific columns (example, adjust as needed)
    df = recast(df, *recast_columns)
    
    # Step 6: Drop rows where all values are NaN
    df = drop_na(df)
    
    # Step 7: Fill NaN values with the mean of specified columns
    df = fill_na_mean(df, *mean_columns)
    
    # Step 8: Fill NaN values based on gender ratio
    df = fill_na_gender_ratio(df, *gender_columns)
    
    # Step 9: Drop duplicates based on specified columns
    df = drop_duplicates(df, *dupe_columns)
    
    return df


"""
column_replacements = {'Old Name': 'New_Name'}
whole_replacements = {'old_value': 'new_value'}
substring_replacements = {'substring': 'replacement'}
char_columns = ['your_column_name1', 'your_column_name2']  # Replace with actual column names
recast_columns = ["column1, column2"]
mean_columns = ['column1', 'column2']
gender_columns = ['gender']
dupe_columns = ['customer_lifetime_value', 'income', 'monthly_premium_auto', 'state', 'policy_type', 'gender']

# Clean the dataset
cleaned_df = clean_dataset(car_insurance_df, column_replacements, whole_replacements, substring_replacements, char_columns, recast_columns, mean_columns, gender_columns, dupe_columns)
"""




import re

def replace_values(df, whole_replacements, substring_replacements):
    """
    df: pandas DataFrame
    whole_replacements: A dictionary for direct replacements.
    substring_replacements: A dictionary where keys are substrings and values are what they should be replaced with.
    """
    df2 = df.copy()

    # Perform whole replacements
    for key, value in whole_replacements.items():
        df2.replace(key, value, inplace=True)

    # Perform substring replacements
    for key, value in substring_replacements.items():
        if isinstance(key, str):
            escaped_key = re.escape(key)  # Escape special characters in the key (like *)
            for col in df2.select_dtypes(include='object').columns:
                df2[col] = df2[col].str.replace(escaped_key, value, regex=True)

                # Add this print statement to debug and check if replacement is happening
                print(f"Replacing '{key}' with '{value}' in column '{col}'")

                # Also print out a few values from the DataFrame to verify
                print(df2[col].head())  # Just for debugging, you can remove this later
    
    return df2


