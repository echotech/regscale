import pytest
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler("test_data_comparison.log")
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def is_same(data1, data2):
    logger.info(f"Starting comparison of data structures")
    
    def compare(d1, d2, path=""):
        if type(d1) != type(d2):
            logger.info(f"Type mismatch at {path}: {type(d1)} vs {type(d2)}")
            return [f"Type and value mismatch at {path}: {repr(d1)} ({type(d1)}) vs {repr(d2)} ({type(d2)})"]
        
        if isinstance(d1, dict):
            logger.info(f"Comparing dictionaries at {path if path else 'root'}")
            differences = []
            all_keys = set(d1.keys()) | set(d2.keys())
            for key in all_keys:
                if key not in d1:
                    logger.info(f"Key '{key}' missing in data1 at {path if path else 'root'}")
                    differences.append(f"Key '{key}' missing in data1 at {path if path else 'root'}")
                elif key not in d2:
                    logger.info(f"Key '{key}' missing in data2 at {path if path else 'root'}")
                    differences.append(f"Key '{key}' missing in data2 at {path if path else 'root'}")
                else:
                    new_path = f"{path}.{key}" if path else key
                    differences.extend(compare(d1[key], d2[key], new_path))
            return differences
        
        elif isinstance(d1, list):
            logger.info(f"Comparing lists at {path if path else 'root'}")
            differences = []
            for i, (v1, v2) in enumerate(zip(d1, d2)):
                new_path = f"{path}[{i}]"
                differences.extend(compare(v1, v2, new_path))
            if len(d1) != len(d2):
                logger.info(f"List length mismatch at {path if path else 'root'}: {len(d1)} vs {len(d2)}")
                differences.append(f"List length mismatch at {path if path else 'root'}: {len(d1)} vs {len(d2)}")
            return differences
        
        elif d1 != d2:
            logger.info(f"Value mismatch at {path if path else 'root'}: {repr(d1)} vs {repr(d2)}")
            return [f"Value mismatch at {path if path else 'root'}: {repr(d1)} vs {repr(d2)}"]
        
        return []

    differences = compare(data1, data2)
    logger.info(f"Comparison completed. Found {len(differences)} differences.")
    return (len(differences) == 0, differences if differences else None)

# Test cases
def test_identical_dicts():
    logger.info("Starting test_identical_dicts")
    data = {'a': 1, 'b': {'c': 2, 'd': [3, 4, 5]}}
    assert is_same(data, data) == (True, None)
    logger.info("Completed test_identical_dicts")

def test_different_types():
    logger.info("Starting test_different_types")
    data1 = {'a': '1'}
    data2 = {'a': 1}
    assert is_same(data1, data2) == (False, ["Type and value mismatch at a: '1' (<class 'str'>) vs 1 (<class 'int'>)"])
    logger.info("Completed test_different_types")

def test_missing_keys():
    logger.info("Starting test_missing_keys")
    data1 = {'a': 1, 'b': 2}
    data2 = {'a': 1}
    assert is_same(data1, data2) == (False, ["Key 'b' missing in data2 at root"])
    logger.info("Completed test_missing_keys")

def test_list_length_mismatch():
    logger.info("Starting test_list_length_mismatch")
    data1 = [1, 2, 3]
    data2 = [1, 2, 3, 4]
    assert is_same(data1, data2) == (False, ["List length mismatch at root: 3 vs 4"])
    logger.info("Completed test_list_length_mismatch")

def test_complex_example():
    logger.info("Starting test_complex_example")
    data1 = {
        'a': '1',
        'b': 2,
        'c': {'a': 1, 'b': [1, 2, 3], 'c': None, 'd': False},
        'd': [1, 2, [3, 4, 5], {'e': 'e1', 'f': 'f1'}, True, None],
        'e': True,
        'f': None
    }
    data2 = {
        'a': 1,
        'b': '2',
        'c': {'a': '1', 'b': [1, 2, 3, 4], 'c': None, 'd': True},
        'd': [1, 2, [3, 4, 5], {'e': 'e1', 'f': 'f1'}, True],
        'e': True
    }
    outcome, differences = is_same(data1, data2)
    assert outcome == False
    assert set(differences) == set([
        "Type and value mismatch at a: '1' (<class 'str'>) vs 1 (<class 'int'>)",
        "Type and value mismatch at b: 2 (<class 'int'>) vs '2' (<class 'str'>)",
        "Type and value mismatch at c.a: 1 (<class 'int'>) vs '1' (<class 'str'>)",
        "List length mismatch at c.b: 3 vs 4",
        "Value mismatch at c.d: False vs True",
        "List length mismatch at d: 6 vs 5",
        "Key 'f' missing in data2 at root"
    ])
    logger.info("Completed test_complex_example")

# Make sure to close the handlers after the test
@pytest.fixture(scope="module", autouse=True)
def close_handlers():
    yield
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

if __name__ == "__main__":
    pytest.main([__file__])