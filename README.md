# RegScale Web Scraping and Data Comparison Test Suite

This test suite includes web scraping tests for the RegScale website and a data comparison utility.

## Features

- Supports multiple browsers (Chrome, Firefox, Edge) for web scraping
- Parameterized tests for different catalog types
- Handles pagination to collect data from multiple pages
- Detailed logging of test execution
- Flexible and easy-to-use test runner
- Data comparison utility for complex nested structures

## Prerequisites

- Python 3.11.6 or later
- pip (Python package installer)

## Setup

1. Clone this repository to your local machine.
2. Navigate to the project directory.

## Running the Web Scraping Tests

To run the web scraping tests, use the `run_tests.py` script:

```
python run_tests.py
```

When prompted, enter the browser you want to use (chrome, firefox, or edge). If you don't specify a browser and simply press enter, Chrome will be used by default.

## Data Comparison Utility

The `test_data_comparison.py` script provides a utility for comparing complex nested data structures.

### Features of the Data Comparison Utility

- Compares two data structures (dictionaries or lists) recursively
- Identifies differences in types, values, missing keys, and list lengths
- Provides detailed path information for each difference found
- Includes logging for debugging and tracking the comparison process

### Running the Data Comparison Tests

To run the data comparison tests:

```
pytest test_data_comparison.py
```

This will run all the test cases defined in the script, including:
- Comparing identical dictionaries
- Detecting different types
- Identifying missing keys
- Finding nested differences
- Detecting list length mismatches
- A complex example with multiple types of differences

### Using the is_same() Function

You can also use the `is_same()` function in your own code to compare data structures:

```python
from test_data_comparison import is_same

data1 = {'a': 1, 'b': [1, 2, 3]}
data2 = {'a': '1', 'b': [1, 2, 3, 4]}

is_identical, differences = is_same(data1, data2)

if is_identical:
    print("The data structures are identical")
else:
    print("Differences found:")
    for diff in differences:
        print(diff)
```

This will output the differences found between the two data structures.

## Logging

Both the web scraping tests and the data comparison utility use Python's logging module. Logs are written to both the console and log files in the project directory.

## Troubleshooting

If you encounter any issues:
1. Check the log files for detailed information about the test runs.
2. Ensure that you have the latest versions of the required packages installed.
3. For web scraping tests, make sure you have the appropriate WebDriver for your chosen browser installed and accessible in your system PATH.

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.