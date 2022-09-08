from gettext import install
import os
import json

import numpy as np
import pandas as pd

from utils import get_project_root, is_date


# Define the datasets path
dataset_path = os.path.join(get_project_root(), "datasets")

# Read in data_config.json
with open(os.path.join(dataset_path, "data_config.json")) as json_file:
    data_config = json.load(json_file)

print()
print("The data config dic is: ", data_config)


original_data_config_keys = ["annual_data", "quarterly_data", "monthly_data", "annual_data_description",
                                 "quarterly_data_description", "monthly_data_description"]


# Check if keys are correct
if not set(data_config) == set(original_data_config_keys):
    raise ValueError(
        "Original 'data_config.json' keys have been changed. Change it back to '" + "', '".join(
        original_data_config_keys) + "'")

# Check data types - Check for other datatypes?
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
                    raise ValueError("Tabular datasets should have at least one column besides the date column")

                # Check if first columns are dates
                if not all(data.iloc[:, 0].apply(lambda x: is_date(x))):
                    raise TypeError("Tabular datasets should have parsable dates as the first column")

                # Set dates as index
                data = data.set_index(data.columns[0])

                # Check for numeric columns
                if len(data.columns[list(map(pd.api.types.is_numeric_dtype, data.dtypes))]) != len(data.columns):
                    raise TypeError("Tabular datasets should have only numeric (int or float) values")

                # Check there is atleast one row entry in all columns
#                if len([col for col in data.columns if len(data[col]) < 2]) == 0:
#                    raise ValueError("Tabular datasets should have at least one column with row entries")

            # Add to data dictionary
            data_dict[key] = data
        
        # If file does not exist, print warning, and return None
        except FileNotFoundError:
            print("'" + filename + "' not found!")
            data_dict[key] = None



print(data_config)
print()
