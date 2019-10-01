"""
Contains the key configuration settings used by the tool
"""
from collections import OrderedDict

#the fields and values constant/common across the output file (ie. not dependent on the row)
COMMON_OUTPUT_VALUES = OrderedDict([
    ("Study","COPD_LIVE"),
    ("site","s01leic"),
    ("Visit Cycle Number","1"),
    ("eForm Code","frm_BloodRes")
])

RESULT_DATE_FIELD = "sample_collection_date_time"
RESULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
RESULT_FIELD = "result"
RESULT_TEST_CODE_FIELD= "local_test_code"
RESULT_STUDY_ID_FIELD= "study_id"

VISIT_DATE_FORMAT="%d-%b-%y"
VISIT_DATE_FIELD='Visit date'
VISIT_STUDY_NO_FIELD = 'Screening Number'
VISIT_NO_FIELD = 'Visit number'

OUTPUT_DATE_FORMAT="%d/%m/%Y"