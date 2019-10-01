import pytest

import lab2macro.data
from lab2macro import core, process, extract, error
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

test_map = lab2macro.data.TestMap([
    {"test_code": "EOSAB", "var_code": "eosinophil"},
    {"test_code": "NEU", "var_code": "neutrophil"},
    {"test_code": "PLT", "var_code": "platelet"}
])

def test_extract_subject_visit_tests_works_with_no_errors():
    test_data1 = test_data.copy()

    visit = lab2macro.data.SubjectVisitDetails(study_id="12345", visit_date=dt.date(2018, 3, 2), visit_no="vst1")
    obs_tests = core.extract_validated_visit_tests(test_data1, visit, test_map)

    exp_tests = [process.ValidatedRow([('Study', 'COPD_LIVE'), ('Site', 's01leic'), ('Subject ID', ""), ('Subject Label', '12345'),
                       ('Visit Code', 'vst1'), ('Visit Cycle Number', 1), ('Visit Date', '02/03/2018'),
                       ('eForm Code', 'frm_BloodRes'), ('eForm Cycle Number', 1), ('eForm Date', ''),
                       ('Question Code', 'eosinophil'), ('Question Cycle', 1), ('Question Value', '0.04'),
                       ('Unobtainable status', ""), ('Username', '')]), process.ValidatedRow(
            [('Study', 'COPD_LIVE'), ('Site', 's01leic'), ('Subject ID', ""), ('Subject Label', '12345'),
             ('Visit Code', 'vst1'), ('Visit Cycle Number', 1), ('Visit Date', '02/03/2018'),
             ('eForm Code', 'frm_BloodRes'), ('eForm Cycle Number', 1), ('eForm Date', ''),
             ('Question Code', 'neutrophil'), ('Question Cycle', 1), ('Question Value', '0.1'),
             ('Unobtainable status', ""), ('Username', '')]), process.ValidatedRow(
            [('Study', 'COPD_LIVE'), ('Site', 's01leic'), ('Subject ID', ""), ('Subject Label', '12345'),
             ('Visit Code', 'vst1'), ('Visit Cycle Number', 1), ('Visit Date', '02/03/2018'),
             ('eForm Code', 'frm_BloodRes'), ('eForm Cycle Number', 1), ('eForm Date', ''),
             ('Question Code', 'platelet'), ('Question Cycle', 1), ('Question Value', ''),
             ('Unobtainable status', 1), ('Username', '')])]

    assert obs_tests.errors == []
    assert obs_tests.data[0] == exp_tests[0]
    assert obs_tests.data[1] == exp_tests[1]

def test_extract_validated_visit_tests_handles_invalid_field_with_non_numeric_result():
    test_data2 = deepcopy(test_data)
    test_data2[3]["result"]=None

    visit = lab2macro.data.SubjectVisitDetails(study_id="12345", visit_date=dt.date(2018, 3, 2), visit_no="1")

    obs_tests = core.extract_validated_visit_tests(test_data2, visit, test_map)

    exp_tests = [
        process.ValidatedRow(
            [('Study', 'COPD_LIVE'), ('Site', 's01leic'), ('Subject ID', ''), ('Subject Label', '12345'),
             ('Visit Code', '1'), ('Visit Cycle Number', 1), ('Visit Date', '02/03/2018'),
             ('eForm Code', 'frm_BloodRes'), ('eForm Cycle Number', 1), ('eForm Date', ''),
             ('Question Code', 'neutrophil'), ('Question Cycle', 1), ('Question Value', '0.1'),
             ('Unobtainable status', ""), ('Username', '')]),
        process.ValidatedRow(
            [('Study', 'COPD_LIVE'), ('Site', 's01leic'), ('Subject ID', ''), ('Subject Label', '12345'),
             ('Visit Code', '1'), ('Visit Cycle Number', 1), ('Visit Date', '02/03/2018'),
             ('eForm Code', 'frm_BloodRes'), ('eForm Cycle Number', 1), ('eForm Date', ''),
             ('Question Code', 'platelet'), ('Question Cycle', 1), ('Question Value', ''),
             ('Unobtainable status', "1"), ('Username', '')])
    ]

    assert obs_tests.data == exp_tests

    assert len(obs_tests.errors) == 1
    assert isinstance(obs_tests.errors[0],error.NonNumericResult)

def test_extract_validated_visit_tests_handles_inconsistent_results():
    test_data3 = deepcopy(test_data)
    test_map = lab2macro.data.TestMap([
        {"test_code": "EOSAB", "var_code": "eosinophil"},
        {"test_code": "NEU", "var_code": "neutrophil"}
    ])

    visit = lab2macro.data.SubjectVisitDetails(study_id="12346", visit_date=dt.date(2018, 3, 2), visit_no="1")

    obs_tests = core.extract_validated_visit_tests(test_data3, visit, test_map)

    assert len(obs_tests.data) == 1

    assert len(obs_tests.errors) == 1
    assert isinstance(obs_tests.errors[0],error.InconsistentResults)
