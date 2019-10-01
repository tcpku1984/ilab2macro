import pytest
from macroload import extract, core
import datetime as dt
import logging as l
l.basicConfig(level=l.INFO)

TEST_CODE = "EOSAB"
TEST_CODE2 = "EOS"
STUDY_ID = "12345"
TEST_DATE = dt.date(2013,3,2)

test_data = [
{"study_id": "12346", "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": "NEU",
                 "result": "0.03"},
{"study_id": STUDY_ID, "sample_collection_date_time": "2012-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id":STUDY_ID,"sample_collection_date_time":"2013-03-02 01:02:03", "local_test_code": TEST_CODE, "result": "0.04"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.06"},
    {"study_id":STUDY_ID,"sample_collection_date_time":"2013-02-29 01:02:03", "local_test_code":"NEU", "result":"0.1"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"},

    ]

def test_it_extracts_all_tests_for_specific_study():
    obs_data = extract.SubjectTests.extract_for_subject(test_data, STUDY_ID)
    exp_data = extract.SubjectTests([

        {"study_id": STUDY_ID, "sample_collection_date_time": "2012-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.04"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.06"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-02-29 01:02:03", "local_test_code": "NEU",
         "result": "0.1"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"}
    ], STUDY_ID)

    assert obs_data == exp_data
    assert isinstance(exp_data, extract.SubjectTests)
    assert obs_data.subject_id == STUDY_ID

def test_it_finds_specific_test_on_supplied_date():
    input_data = extract.SubjectTests([

        {"study_id": STUDY_ID, "sample_collection_date_time": "2012-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.04"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.06"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-02-29 01:02:03", "local_test_code": "NEU",
         "result": "0.1"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"}
    ], STUDY_ID)

    obs_data = extract.DatedSubjectSpecificTests.extract_specific_tests_with_date(input_data,[TEST_CODE], TEST_DATE)
    exp_data = extract.DatedSubjectSpecificTests([
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "parsed_date": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.04"},
    ], STUDY_ID, TEST_CODE, TEST_DATE)

    assert isinstance(exp_data, extract.DatedSubjectSpecificTests)
    assert list(obs_data) == list(exp_data)

def test_it_finds_specific_tests_on_supplied_date():
    input_data = extract.SubjectTests([

        {"study_id": STUDY_ID, "sample_collection_date_time": "2012-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.04"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "local_test_code": TEST_CODE2,
         "result": "0.05"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": TEST_CODE,
         "result": "0.06"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-02-29 01:02:03", "local_test_code": "NEU",
         "result": "0.1"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"}
    ], STUDY_ID)

    obs_data = extract.DatedSubjectSpecificTests.extract_specific_tests_with_date(input_data,[TEST_CODE,TEST_CODE2], TEST_DATE)
    exp_data = extract.DatedSubjectSpecificTests([
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "parsed_date": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.04"},{"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02 01:02:03", "parsed_date": "02/03/2013", "local_test_code": TEST_CODE2,
         "result": "0.05"}
    ], STUDY_ID, TEST_CODE, TEST_DATE)

    assert isinstance(exp_data, extract.DatedSubjectSpecificTests)
    assert list(obs_data) == list(exp_data)

def test_it_raises_exception_during_validation_if_values_are_different():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": STUDY_ID, "sample_collection_date_time": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.04"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.06"},
    ], STUDY_ID, TEST_DATE, TEST_CODE)

    with pytest.raises(extract.InconsistentResults):
        extract.validate_rows(input_data)

def test_it_returns_empty_test_if_no_values():
    input_data = extract.DatedSubjectSpecificTests([], STUDY_ID, TEST_DATE, [TEST_CODE])

    obs_row = extract.validate_rows(input_data)

    assert obs_row.subject_id == STUDY_ID
    assert obs_row.test_code == TEST_CODE
    assert obs_row.test_date == TEST_DATE
    assert obs_row.result == ""
    assert obs_row.unobtainable_status == "1"

def test_it_returns_single_test_if_values_are_same():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": STUDY_ID, "sample_collection_date_time": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.04"},
        {"study_id": STUDY_ID, "sample_collection_date_time": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.04"},
    ], STUDY_ID, TEST_DATE, TEST_CODE)

    obs_row = extract.validate_rows(input_data)

    assert obs_row.subject_id == STUDY_ID
    assert obs_row.test_code == TEST_CODE
    assert obs_row.test_date == TEST_DATE
    assert obs_row.result == "0.04"
    assert obs_row.unobtainable_status == ""

def test_it_returns_single_test_if_single_row():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": STUDY_ID, "sample_collection_date_time": "02/03/2013", "local_test_code": TEST_CODE,
         "result": "0.05"}
    ],STUDY_ID, TEST_DATE, TEST_CODE)


    obs_row = extract.validate_rows(input_data)

    assert obs_row.subject_id == STUDY_ID
    assert obs_row.test_code == TEST_CODE
    assert obs_row.test_date == TEST_DATE
    assert obs_row.result == "0.05"
    assert obs_row.unobtainable_status == ""

def test_it_returns_number_if_gt_sign_in_front():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ">3.00"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ">3.00"}
    )
    obs_row = extract.validate_rows(input_data, core.TestInfo("eosinophil",0,4))

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
    obs_row = extract.validate_rows(input_data, core.TestInfo("eosinophil",0,3))

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
    obs_row = extract.validate_rows(input_data, core.TestInfo("eosinophil",-50,0))

    assert exp_row == obs_row

def test_it_raises_exception_during_validation_if_text_value():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "POS"}
    ])

    with pytest.raises(macroload.error.NonNumericResult):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",0,1))


def test_it_raises_exception_during_validation_if_empty_value():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ""}
    ])

    with pytest.raises(macroload.error.NonNumericResult):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",0,1))

def test_it_raises_exception_during_validation_if_below_min_value():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.09"}
    ])

    with pytest.raises(macroload.error.NumberOutOfRange):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",0.1,0.3))

def test_it_raises_exception_during_validation_if_above_max_value():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "0.31"}
    ])

    with pytest.raises(macroload.error.NumberOutOfRange):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",0.1,0.3))


def test_it_raises_exception_during_validation_if_below_min_value_which_is_negative():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "-6"}
    ])

    with pytest.raises(macroload.error.NumberOutOfRange):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",-5,0.3))

def test_it_raises_exception_during_validation_if_below_min_value_which_has_less_than_prefix():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "<5.99"}
    ])

    with pytest.raises(macroload.error.NumberOutOfRange):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",6,7))

def test_it_raises_exception_during_validation_if_above_max_value_which_has_greater_than_prefix():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": ">200"}
    ])

    with pytest.raises(macroload.error.NumberOutOfRange):
        extract.validate_rows(input_data, core.TestInfo("eosinophil",5,199.99))

def test_it_allows_large_number_if_no_maximum():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "100000"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "100000"}
    )
    obs_row = extract.validate_rows(input_data, core.TestInfo("eosinophil",0,None))

    assert exp_row == obs_row

def test_it_allows_exact_number_if_maximum():
    input_data = extract.DatedSubjectSpecificTests([
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "50"}
    ])

    exp_row = extract.ValidatedSubjectSpecificTest(
        {"study_id": "12345", "sample_collection_date_time": "02/03/2013", "local_test_code": "EOSAB",
         "result": "50"}
    )
    obs_row = extract.validate_rows(input_data, core.TestInfo("eosinophil",0,50))

    assert exp_row == obs_row