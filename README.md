# lab2macro
![](https://github.com/rcfgroup/ilab2macro/workflows/main/badge.svg)

This is a simple Python 3.4+ script which uses pseudonymised lab test data to generate an output file which can be loaded into Infermed MACRO. To do this it uses three CSV-based input files:

- visits: (fields arranged as Participant ID,Screening Number,Visit number,Visit date)
- test set: (fields most contain lab test_code, macro var_code, min (optional) and max (optional))
- test data: (fields can be configured by changing the `config.py` file)

The script is run by using:

`lab2macro.py`

The parameters are:
```
  --visits PATH  Name of visits file in CSV format (fields arranged as
                 Participant ID,Screening Number,Visit number,Visit date)
                 [required]
  --tests PATH   Name of test set file in CSV format (fields most contain
                 test_code,var_code)  [required]
  --data PATH    Name of input data file in tab-delimited format (fields can be
                 configured by changing the `config.py` file)  [required]
  --output TEXT  Output file for MACRO data  [required]
  --help         Show this message and exit.
```

## SETUP

It is recommended it is run using a virtualenv although it should work without.
To install dependencies:
`pip install -r requirements.txt`

The tool has also been statically type checked using mypy and unittests written using pytest.
