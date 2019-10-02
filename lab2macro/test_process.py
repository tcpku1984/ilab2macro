import lab2macro.result
from lab2macro import process, config, extract, error, data, result
import datetime as dt
import pytest
from collections import OrderedDict

RESULT = "0.04"
STUDY_ID = "12345"
VISIT_CODE = "vsT0"
TEST_DATE = dt.date(2013,3,2)
TEST_CODE="EOSAB"
TEST_CODE2 = "EOS"

test_map = data.TestMap([
    {"test_code":"EOSAB","var_code":"eosinophil"},
    {"test_code":"EOS","var_code":"eosinophil"},
    {"test_code":"NEU","var_code":"neutrophil"}
])

def test_create_output_row():
    row = result.ValidatedResult(extract.DatedSubjectSpecificTests([
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02", "local_test_code": TEST_CODE2,
         "result": RESULT}],STUDY_ID, TEST_DATE,TEST_CODE)
    )
    visit_details = data.SubjectVisitDetails(study_id = STUDY_ID, visit_no=VISIT_CODE, visit_date = TEST_DATE)
    obs_prow = process.create_processed_row(row, visit_details, test_map.info_for_test_code(TEST_CODE2))

    exp_data = config.INITIAL_ROW.copy()

    exp_data.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Cycle Number": 1,
        "Visit Date": TEST_DATE.strftime(config.OUTPUT_DATE_FORMAT),
        "eForm Code":"frm_BloodRes",
        "eForm Cycle Number":1,
        "Question Code":"eosinophil",
        "Question Value": "0.04",
        "Unobtainable status":"",
    })
    exp_prow = process.ProcessedRow(exp_data)
    assert obs_prow == exp_prow

def test_validate_output_row_raises_exception_if_no_result():
    row = config.INITIAL_ROW.copy()

    row.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Cycle Number": '1',
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":"eosinophil",
        "Question Cycle": None
    })

    with pytest.raises(error.RequiredField):
        process.validate_required_fields(process.ProcessedRow(row))

def test_validate_output_row_raises_exception_if_no_code():
    row = config.INITIAL_ROW.copy()

    row.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":None,
        "Question Value": 0.06
    })

    with pytest.raises(error.RequiredField):
        process.validate_required_fields(process.ProcessedRow(row))

def test_validate_output_row_returns_validated_row():
    row = config.INITIAL_ROW.copy()

    row.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":"eosino",
        "Question Value": 0.06
    })

    obs_row = process.validate_required_fields(process.ProcessedRow(row))
    exp_row = process.ValidatedRow(row)
    assert list(obs_row.keys()) == ["Study",
                                    "Site",
                                    "Subject ID",
                                    "Subject Label",
                                    "Visit Code",
                                    "Visit Cycle Number",
                                    "Visit Date",
                                    "eForm Code",
                                    "eForm Cycle Number",
                                    "eForm Date",
                                    "Question Code",
                                    "Question Cycle",
                                    "Question Value",
                                    "Unobtainable status",
                                    "Username"
                                    ]
    assert obs_row == exp_row
    assert isinstance(obs_row, process.ValidatedRow)





