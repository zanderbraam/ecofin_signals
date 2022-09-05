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
