# ecofin_signals
Tools for creating leading economic signals from raw economic data

After cloning the repository, create a virtual environment.
A virtual environment creates a sandbox that does not affect the system Python.

```
virtualenv ve -p `which python3.6`
source ./ve/bin/activate
pip install numpy
pip install -r requirements.txt
```

**Note:** Datasets (in CSV format) are required in the `datasets` directory and will not be hosted in this repository.
Please procure datasets from your own source.

## Expected data
Add datasets in the `datasets` directory, and pass them through in the `data_config.json` file:

```yaml
{
    "annual_data": "xxx1.csv",
    "quarterly_data": "xxx2.csv",
    "monthly_data": "xxx3.csv",
    "annual_data_description": "xxx4.csv",
    "quarterly_data_description": "xxx5.csv",
    "monthly_data_description": "xxx6.csv"
}
```

If a dataset is not available, add an empty string, `""` to `data_config.json` where necessary.
