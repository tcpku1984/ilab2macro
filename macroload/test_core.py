from macroload import core, error
import datetime as dt
import logging as l
from collections import OrderedDict
l.basicConfig(level=l.INFO)

from copy import deepcopy

test_data = [
{"study_id": "12346", "sample_collection_date_time": "2018-03-02 01:02:03", "local_test_code": "NEU",
                 "result": "0.03"},
{"study_id": "12346", "sample_collection_date_time": "2018-03-02 01:02:03", "local_test_code": "NEU",
                 "result": "0.05"},
{"study_id": "12345", "sample_collection_date_time": "2018-01-02 01:02:03", "local_test_code": "NEU",
         "result": "0.09"},
        {"study_id":"12345","sample_collection_date_time":"2018-03-02 01:02:03", "local_test_code":"EOSAB", "result":"0.04"},
        {"study_id": "12345", "sample_collection_date_time": "2018-03-05 01:02:03", "local_test_code": "EOSAB",
         "result": "0.06"},
    {"study_id":"12345","sample_collection_date_time":"2018-03-02 14:03:11", "local_test_code":"NEU", "result":"0.1"},
        {"study_id": "12345", "sample_collection_date_time": "2018-03-05 01:02:03", "local_test_code": "NEU",
         "result": "0.10"},
{"study_id": "12346", "sample_collection_date_time": "2018-03-02 01:02:03", "local_test_code": "EOSAB",
         "result": "0.07"},
    ]

test_map = OrderedDict([
        ("EOSAB","eosinophil"),
        ("NEU","neutrophil")
    ])

def test_extract_subject_visit_tests_works_with_no_errors():
    test_data1 = test_data.copy()

    visit = core.SubjectVisitDetails(study_id="12345", visit_date=dt.date(2018, 3, 2), visit_no="1")
    obs_tests = core.extract_validated_visit_tests(test_data1, visit, test_map)

    exp_tests = [{'Study': 'COPD_LIVE', 'eForm Code': 'frm_BloodRes', 'Visit Code': '1', 'Question Cycle': '0.04', 'Subject Label': '12345', 'Visit Cycle Number': '1', 'Visit Date': '02/03/2018', 'site': 's01leic', 'Question Code': 'eosinophil'},{'Study': 'COPD_LIVE', 'eForm Code': 'frm_BloodRes', 'Visit Code': '1', 'Question Cycle': '0.1', 'Subject Label': '12345', 'Visit Cycle Number': '1', 'Visit Date': '02/03/2018', 'site': 's01leic', 'Question Code': 'neutrophil'}]

    assert obs_tests.errors == []
    assert dict(obs_tests.data[0]) == dict(exp_tests[0])
    assert dict(obs_tests.data[1]) == dict(exp_tests[1])

def test_extract_validated_visit_tests_handles_invalid_field():
    test_data2 = deepcopy(test_data)
    test_data2[3]["result"] = None

    visit = core.SubjectVisitDetails(study_id="12345", visit_date=dt.date(2018, 3, 2), visit_no="1")

    obs_tests = core.extract_validated_visit_tests(test_data2, visit, test_map)

    exp_tests = [{'Study': 'COPD_LIVE', 'eForm Code': 'frm_BloodRes', 'Visit Code': '1', 'Question Cycle': '0.1',
                  'Subject Label': '12345', 'Visit Cycle Number': '1', 'Visit Date': '02/03/2018', 'site': 's01leic',
                  'Question Code': 'neutrophil'}]

    assert dict(obs_tests.data[0]) == dict(exp_tests[0])
    assert len(obs_tests.data) == 1
    assert len(obs_tests.errors) == 1
    assert isinstance(obs_tests.errors[0], error.NonNumericResult)

def test_extract_validated_visit_tests_handles_inconsistent_results():
    test_data3 = deepcopy(test_data)

    test_map = OrderedDict([
        ("EOSAB","eosinophil"),
        ("NEU","neutrophil")
    ])
    visit = core.SubjectVisitDetails(study_id="12346", visit_date=dt.date(2018, 3, 2), visit_no="1")

    obs_tests = core.extract_validated_visit_tests(test_data3, visit, test_map)

    assert len(obs_tests.data) == 1

    assert len(obs_tests.errors) == 1
    assert isinstance(obs_tests.errors[0], error.InconsistentResults)

def test_extract_validated_visit_handles_no_test_code():
    test_data3 = deepcopy(test_data)

    test_map = OrderedDict([
        ("EOSAB","eosinophil"),
        (None,"neutrophil")
    ])
    visit = core.SubjectVisitDetails(study_id="12346", visit_date=dt.date(2018, 3, 2), visit_no="1")

    obs_tests = core.extract_validated_visit_tests(test_data3, visit, test_map)

    assert len(obs_tests.data) == 1

    assert len(obs_tests.errors) == 1
    assert isinstance(obs_tests.errors[0], error.InvalidTestCode)

def test_extract_validated_visit_handles_no_test_code_and_inconsistent_result():
    test_data3 = deepcopy(test_data)

    test_map = OrderedDict([
        (None,"eosinophil"),
        ("NEU","neutrophil")
    ])
    visit = core.SubjectVisitDetails(study_id="12346", visit_date=dt.date(2018, 3, 2), visit_no="1")

    obs_tests = core.extract_validated_visit_tests(test_data3, visit, test_map)

    assert len(obs_tests.data) == 0

    assert len(obs_tests.errors) == 2
    assert isinstance(obs_tests.errors[0], error.InvalidTestCode)
    assert isinstance(obs_tests.errors[1], error.InconsistentResults)