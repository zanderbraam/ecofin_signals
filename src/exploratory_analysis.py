import os
import json

import numpy as np
import pandas as pd

from src.utils import get_project_root, is_date


def get_raw_data():
    """
    Fetches raw data from the datasets directory, based on data_config.json

    :return: dictionary of pd.DataFrames
    """

    # Define the datasets path
    dataset_path = os.path.join(get_project_root(), "datasets")

    # Read in data_config.json
    with open(os.path.join(dataset_path, "data_config.json")) as json_file:
        data_config = json.load(json_file)

    original_data_config_keys = ["annual_data", "quarterly_data", "monthly_data", "annual_data_description",
                                 "quarterly_data_description", "monthly_data_description"]
    # Check if keys are correct
    if not set(data_config) == set(original_data_config_keys):
        raise ValueError(
            "Original 'data_config.json' keys have been changed. Change it back to '" + "', '".join(
                original_data_config_keys) + "'")

    # Check data types
    if not all(type(value) == str for value in data_config.values()):
        raise TypeError("Please provide strings corresponding to data filenames")

    # Initialize empty dictionary
    data_dict = {}

    # Fill dictionary by reading in data
    for key, filename in data_config.items():

        # Check for empty strings
        if len(filename) == 0:
            data_dict[key] = None
        else:
            # Try reading in data
            try:
                data = pd.read_csv(os.path.join(dataset_path, filename))

                if "description" in key:
                    # Check columns for correct format
                    if len(data.columns) != 2:
                        raise ValueError("A description dataset should contain only 2 columns: one with column heading "
                                         "and another for the description")
                else:
                    # Check for number of columns
                    if len(data.columns) < 2:
                        raise ValueError("Tabular datasets should have at least one column besides the date index")

                    # Check if first columns are dates
                    if not all(data.iloc[:, 0].apply(lambda x: is_date(x))):
                        raise TypeError("Tabular datasets should have parsable dates as the first column")

                    # Set dates as index
                    data = data.set_index(data.columns[0])

                    # Check for numeric columns
                    if len(data.columns[list(map(pd.api.types.is_numeric_dtype, data.dtypes))]) != len(data.columns):
                        raise TypeError("Tabular datasets should have only numeric (int or float) values")

                # Add to data dictionary
                data_dict[key] = data

            # If file does not exist, print warning, and return None
            except FileNotFoundError:
                print("'" + filename + "' not found!")
                data_dict[key] = None

    # Final check to see if description datasets and tabular datasets match up
    for period in ["annual", "quarter", "month"]:
        relevant_keys = [key for key in data_dict if period in key]
        if len(relevant_keys) == 2:
            descriptive_data = data_dict[[key for key in relevant_keys if "description" in key][0]]
            tabular_data = data_dict[[key for key in relevant_keys if "description" not in key][0]]

            # Check if dict values are set to None
            if all(d is not None for d in [descriptive_data, tabular_data]):

                # If columns and descriptions don't match, raise error
                if len(set(descriptive_data.iloc[:, 0].apply(lambda x: str(x))) - set(tabular_data.columns)) != 0:
                    raise ValueError("Descriptive data does not match the columns of the tabular data!")

        else:
            raise ValueError(
                "Original 'data_config.json' keys have been changed. Change it back to '" + "', '".join(
                    original_data_config_keys) + "'")

    return data_dict


if __name__ == "__main__":
    test_data = get_raw_data()
    print(test_data)
