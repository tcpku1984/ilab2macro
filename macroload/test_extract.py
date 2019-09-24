import pytest

import macroload.error
from macroload import extract
import datetime as dt

test_data = [
{"study_id": "12346", "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": "NEU",
                 "result": "0.03"},
{"study_id": "12345", "sample_collection_date_time": "2012-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id":"12345","sample_collection_date_time":"2013-03-02 01:02:03", "local_test_code":"EOSAB", "result":"0.04"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "EOSAB",
         "result": "0.06"},
    {"study_id":"12345","sample_collection_date_time":"2013-02-29 01:02:03", "local_test_code":"NEU", "result":"0.1"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"},

    ]

def test_it_extracts_all_tests_for_specific_study():
    obs_data = extract.extract_subject_tests(test_data,"12345")
    exp_data = extract.SubjectTests([

        {"study_id": "12345", "sample_collection_date_time": "2012-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "EOSAB",
         "result": "0.06"},
        {"study_id": "12345", "sample_collection_date_time": "2013-02-29 01:02:03", "local_test_code": "NEU",
         "result": "0.1"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"}
    ])

    assert obs_data == exp_data
    assert isinstance(exp_data, extract.SubjectTests)

def test_it_extracts_specific_test_for_specific_study():
    obs_data = extract.extract_specific_tests(test_data,"EOSAB")
    exp_data = extract.SubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "EOSAB",
         "result": "0.06"}
    ])

    assert obs_data == exp_data
    assert isinstance(exp_data, extract.SubjectSpecificTests)

def test_it_parses_subject_tests_date():
    input_data = extract.SubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": "EOSAB",
         "result": "0.06"},
    ])

    obs_data = extract.parse_subject_tests_date(input_data)
    exp_data = extract.ParsedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.06"},
    ])

    assert obs_data == exp_data
    assert isinstance(exp_data, extract.ParsedSubjectSpecificTests)

def test_it_finds_tests_on_specific_date():
    input_data = extract.ParsedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "05/03/2013", "local_test_code": "EOSAB",
         "result": "0.06"},
    ])
    input_date = dt.date(2013,3,5)

    obs_data = extract.extract_rows_with_date(input_data,input_date)
    exp_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "05/03/2013", "local_test_code": "EOSAB",
         "result": "0.06"},
    ])

    assert obs_data == exp_data
    assert isinstance(exp_data, extract.DatedSubjectSpecificTests)

def test_it_raises_exception_during_validation_if_values_are_different():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.06"},
    ])

    with pytest.raises(macroload.error.InconsistentResults):
        extract.validate_rows(input_data)

def test_it_raises_exception_during_validation_if_no_values():
    input_data = extract.DatedSubjectSpecificTests([])

    with pytest.raises(macroload.error.NoResults):
        extract.validate_rows(input_data)

def test_it_returns_single_test_if_values_are_same():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"},
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"},
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"}
    )
    obs_row = extract.validate_rows(input_data)

    assert exp_row == obs_row

def test_it_returns_single_test_if_single_row():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.04"}
    )
    obs_row = extract.validate_rows(input_data)

    assert exp_row == obs_row

def test_it_returns_number_if_gt_sign_in_front():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ">3.00"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ">3.00"}
    )
    obs_row = extract.validate_rows(input_data)

    assert exp_row == obs_row

def test_it_returns_number_if_lt_sign_in_front():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "<0.04"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "<0.04"}
    )
    obs_row = extract.validate_rows(input_data)

    assert exp_row == obs_row


def test_it_returns_number_if_minus_sign_in_front():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "-29.2"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "-29.2"}
    )
    obs_row = extract.validate_rows(input_data)

    assert exp_row == obs_row

def test_it_raises_exception_during_validation_if_text_value():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "POS"}
    ])

    with pytest.raises(macroload.error.NonNumericResult):
        extract.validate_rows(input_data)


def test_it_raises_exception_during_validation_if_empty_value():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ""}
    ])

    with pytest.raises(macroload.error.NonNumericResult):
        extract.validate_rows(input_data)