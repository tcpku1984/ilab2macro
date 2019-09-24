import macroload.error
from macroload import process, config, extract, core
import datetime as dt
import pytest
from collections import OrderedDict

RESULT = "0.04"
STUDY_ID = "12345"
VISIT_CODE = "vsT0"

field_map = OrderedDict([
    ("EOSAB","eosinophil"),
    ("NEU","neutrophil")
    ])

def test_create_output_row():
    row = extract.ValidatedSubjectSpecificTest(
        {"study_id": STUDY_ID, "sample_collection_date_time": "2013-03-02", "local_test_code": "EOSAB",
         "result": RESULT}
    )
    visit_details = core.SubjectVisitDetails(study_id = STUDY_ID, visit_no=VISIT_CODE, visit_date = dt.date(2013,3,2))
    obs_prow = process.create_processed_row(row, visit_details, field_map)

    exp_data = config.COMMON_OUTPUT_VALUES.copy()

    exp_data.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Cycle Number": '1',
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":"eosinophil",
        "Question Cycle": "0.04"
    })
    exp_prow = process.ProcessedRow(exp_data)
    assert dict(obs_prow) == dict(exp_prow)

def test_validate_output_row_raises_exception_if_no_result():
    row = config.COMMON_OUTPUT_VALUES.copy()

    row.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Cycle Number": '1',
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":"eosinophil",
        "Question Cycle": None
    })

    with pytest.raises(macroload.error.NotNoneableField):
        process.validate_row(process.ProcessedRow(row))

def test_validate_output_row_raises_exception_if_no_code():
    row = config.COMMON_OUTPUT_VALUES.copy()

    row.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Cycle Number": '1',
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":None,
        "Question Cycle": 0.06
    })

    with pytest.raises(macroload.error.NotNoneableField):
        process.validate_row(process.ProcessedRow(row))

def test_validate_output_row_returns_validated_row():
    row = config.COMMON_OUTPUT_VALUES.copy()

    row.update({
        "Subject Label":STUDY_ID,
        "Visit Code": VISIT_CODE,
        "Visit Cycle Number": '1',
        "Visit Date": "02/03/2013",
        "eForm Code":"frm_BloodRes",
        "Question Code":"eosino",
        "Question Cycle": 0.06
    })

    obs_row = process.validate_row(process.ProcessedRow(row))
    exp_row = process.ValidatedRow(row)
    assert obs_row == exp_row
    assert isinstance(obs_row, process.ValidatedRow)





