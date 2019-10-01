from lab2macro import data
import pytest

def test_create_test_map_from_rows_handles_multiple_codes_correctly():
    tests = [
        {"var_code": "Eosinophils", "test_code": "EOSAB", "min": "6", "max": "10"},
        {"var_code": "Eosinophils", "test_code": "EOS", "min": "6", "max": "10"},
        {"var_code": "Neutrophils", "test_code": "NEUAB", "min": "8", "max": None},
        {"var_code": "Platelets", "test_code": "PLT", "min": None, "max": "200"}
    ]
    test_map = data.TestMap(tests)

    assert test_map["Eosinophils"] == data.TestInfo("Eosinophils", ["EOSAB","EOS"], 6, 10)
    assert test_map["Neutrophils"] == data.TestInfo("Neutrophils", ["NEUAB"],8, None)
    assert test_map["Platelets"] == data.TestInfo("Platelets", ["PLT"], None, 200)

def test_create_test_map_from_rows_handles_missing_codes_correctly():
    tests = [
        {"var_code": "Eosinophils", "test_code": "", "min": "6", "max": "10"},
        {"var_code": "Eosinophils", "test_code": "EOS", "min": "6", "max": "10"},
        {"var_code": "Neutrophils", "test_code": "NEUAB", "min": "8", "max": None},
        {"var_code": "Platelets", "test_code": "PLT", "min": None, "max": "200"}
    ]

    with pytest.raises(ValueError):
        data.TestMap(tests)

def test_correct_test_info_is_returned_for_different_and_same_codes():
    tests = data.TestMap([
        {"var_code": "Eosinophils", "test_code": "EOSAB", "min": "6", "max": "10"},
        {"var_code": "Eosinophils", "test_code": "EOS", "min": "6", "max": "10"},
        {"var_code": "Neutrophils", "test_code": "NEUAB", "min": "8", "max": None},
        {"var_code": "Platelets", "test_code": "PLT", "min": None, "max": "200"}
    ])
    assert tests.info_for_test_code("EOSAB") == data.TestInfo("Eosinophils", ["EOSAB", "EOS"], 6, 10)
    assert tests.info_for_test_code("EOS") == data.TestInfo("Eosinophils", ["EOSAB", "EOS"], 6, 10)
    assert tests.info_for_test_code("NEUAB") == data.TestInfo("Neutrophils", ["NEUAB"], 8, None)
    assert tests.info_for_test_code("PLT") == data.TestInfo("Platelets", ["PLT"], None, 200)

