"""
Contains the key configuration settings used by the tool
"""
from collections import OrderedDict

#the fields and values constant/common across the output file (ie. not dependent on the row)
INITIAL_ROW = OrderedDict([
    ("Study","COPD_LIVE"),
    ("Site","s01leic"),
    ("Subject ID",""),
    ("Subject Label", None),
    ("Visit Code", None),
    ("Visit Cycle Number", 1),
    ("Visit Date", None),
    ("eForm Code","frm_BloodRes"),
    ("eForm Cycle Number", 1),
    ("eForm Date",""),
    ("Question Code",None),
    ("Question Cycle",1),
    ("Question Value", None),
    ("Unobtainable status",None),
    ("Username","")
])

RESULT_DATE_FIELD = "sample_collection_date_time"
RESULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
RESULT_PARSED_DATE_FIELD = "parsed_date"
RESULT_FIELD = "result"
RESULT_TEST_CODE_FIELD= "local_test_code"
RESULT_STUDY_ID_FIELD= "study_id"

VISIT_DATE_FORMAT="%Y-%m-%d"
VISIT_DATE_FIELD='Visit date'
VISIT_STUDY_ID_FIELD = 'Participant ID'
VISIT_NO_FIELD = 'Visit number'

OUTPUT_DATE_FORMAT="%d/%m/%Y"