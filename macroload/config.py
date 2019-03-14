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

DATE_FIELD = "sample_collection_date_time"
RESULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
RESULT_FIELD = "result"
TEST_CODE_FIELD="local_test_code"
STUDY_ID_FIELD="study_id"
DATE_OUTPUT_FORMAT="%d/%m/%Y"
VISIT_DATE_FORMAT="%d-%b-%y"

