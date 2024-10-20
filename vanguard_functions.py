import numpy as np
import pandas as pd

def strip_replace_ws (df):
    df.columns = df.columns.str.lower().str.replace(" ","_")
    return df


def rename_columns (df, column_replacements):
    """
    column_replacements = {'Old Name': 'New_Name
    """
    df.rename(columns=column_replacements, inplace=True)
    return df


def recast(df, *column_names):
    for column_name in column_names:
        if column_name in df.columns:

            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
            df[column_name] = df[column_name].round(0).astype('Int64')
        else:
            raise KeyError(f"Column '{column_name}' not found in the DataFrame")

    return df


def calculate_completion_rate(df, id_col='visit_id', step_col='process_step', completion_step='confirm'):
    """
    Calculate the completion rate for a given group of users.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing the visit IDs and process steps.
    id_col (str): Column name for IDs. Default is 'visit_id'.
    step_col (str): Column name for the process steps. Default is 'process_step'.
    completion_step (str): The step that marks completion. Default is 'confirm'.

    Returns:
    float: Completion rate as a percentage.
    """
    # Get the total number of unique users
    total_users = df[id_col].nunique()

    # Get the number of users who completed the process (i.e., reached the completion step)
    completed_users = df[df[step_col] == completion_step][id_col].nunique()

    # Calculate the completion rate as a percentage
    completion_rate = round((completed_users / total_users) * 100, 2)

    return completion_rate


def calculate_time_spent_per_step(df, id_col='visit_id', datetime_col='date_time', insert_position=5):
    """
    Calculate the time spent on each step of a visit and returns the modified DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing visit_id and datetime columns.
    id_col (str): Name of the column representing the IDs. Default is 'visit_id'.
    datetime_col (str): Name of the column representing the timestamp. Default is 'date_time'.
    insert_position (int): Position at which to insert the new 'time_spent_seconds' column. Default is 5.

    Returns:
    pd.DataFrame: DataFrame with added 'time_spent_seconds' column, representing time spent on each step.
    """
    # Sort DataFrame by visit ID and timestamp
    df_timesort = df.sort_values(by=[id_col, datetime_col])

    # Calculate the difference in time between consecutive rows for each visit
    df_timesort['time_diff_seconds'] = df_timesort.groupby(id_col)[datetime_col].diff().dt.total_seconds()

    # Shift the time differences to reflect the time spent on the current row
    df_timesort['time_spent_seconds'] = df_timesort['time_diff_seconds'].shift(-1)

    # Move the 'time_spent_seconds' column to a specified position
    time_spent_column = df_timesort.pop('time_spent_seconds')
    df_timesort.insert(insert_position, 'time_spent_seconds', time_spent_column)

    return df_timesort


def calculate_error_rate(df, id_col='visit_id', datetime_col='date_time', step_col='process_step', step_mapping=None):
    """
    Calculate the error rate in the process flow based on step transitions.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing visit IDs, timestamps, and steps.
    id_col (str): Column name for the visit IDs. Default is 'visit_id'.
    datetime_col (str): Column name for the timestamps. Default is 'date_time'.
    step_col (str): Column name for the steps. Default is 'process_step'.
    step_mapping (dict): A dictionary mapping step order to step names. Default is None.

    Returns:
    tuple: A tuple containing the modified DataFrame with added 'errors' column, 
           the total number of errors, and the error rate (in percentage).
    """
    if step_mapping is None:
        step_mapping = {0: 'start', 1: 'step_1', 2: 'step_2', 3: 'step_3', 4: 'confirm'}
    
    # Create reverse mapping to map steps to their numerical order
    reverse_step_mapping = {value: key for key, value in step_mapping.items()}

    # Ensure the 'date_time' column is in datetime format
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    # Map the steps to their numeric order
    df['step_order'] = df[step_col].map(reverse_step_mapping)

    # Sort the DataFrame by visit ID and timestamp to ensure chronological order
    df = df.sort_values(by=[id_col, datetime_col])

    # Detect errors: a step is an error if the step order decreases (non-chronological step transition)
    df['errors'] = df.groupby(id_col)['step_order'].diff() < 0

    # Calculate total errors and total actions
    total_errors = df['errors'].sum()
    total_actions = df.shape[0]

    # Calculate the error rate as a percentage
    error_rate = round((total_errors / total_actions) * 100, 2)

    return df, total_errors, error_rate


def tukeys_test_outliers(my_data, column_name, method="show"):
    # Ensure that the input is a DataFrame and access specific column
    data = my_data[column_name].copy()
    
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds for the outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identify the outliers
    outliers = (data < lower_bound) | (data > upper_bound)

    if method == "show":
        return data[outliers]  # This shows the outliers
    elif method == "replace":
        median = data.median()
        data[outliers] = median  # Replace outliers with median
        my_data[column_name] = data  # Update the DataFrame
        return my_data  # Return modified DataFrame
    elif method == "delete":
        # Filter the DataFrame to keep non-outlier rows
        data_no_outliers = my_data[~outliers]  # Keep rows that are not outliers
        return data_no_outliers  # Return DataFrame without outliers


def cohen_h(p1, p2):
    """Calculate Cohen's h for two proportions."""
    return 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))


def cohen_d(control, test):
    # Calculate the means
    mean_control = np.mean(control)
    mean_test = np.mean(test)
    
    # Calculate the standard deviations
    std_control = np.std(control, ddof=1)  # ddof=1 for sample standard deviation
    std_test = np.std(test, ddof=1)
    
    # Calculate the number of observations in each group
    n_control = len(control)
    n_test = len(test)
    
    # Calculate the pooled standard deviation
    pooled_std = np.sqrt(((n_control - 1) * std_control**2 + (n_test - 1) * std_test**2) / (n_control + n_test - 2))
    
    # Calculate Cohen's d
    d = (mean_control - mean_test) / pooled_std
    
    return d
