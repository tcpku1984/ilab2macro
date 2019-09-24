from macroload import extract, config, core

from collections import OrderedDict
from typing import Dict

from macroload.error import NotNoneableField


class ProcessedRow(OrderedDict):
    """
    Represents a processed row (see create_processed_row)
    """
    pass

class ValidatedRow(OrderedDict):
    """
    Represents a processed row which has been validated
    """
    pass


def create_processed_row(data:extract.ValidatedSubjectSpecificTest, visit: "core.SubjectVisitDetails", field_map:Dict[str,str])->ProcessedRow:
    """
    Creates processed row by amalgamating the visit info, the validated test and the config.COMMON_OUTPUT_VALUES
    :param data:
    :param visit:
    :param field_map:
    :return:
    """
    init_data = config.COMMON_OUTPUT_VALUES.copy()
    test_code = data.get(config.TEST_CODE_FIELD)
    init_data.update(OrderedDict([  #type: ignore
        ("Subject Label", visit.study_id),
        ("Visit Code", visit.visit_no),
        ("Visit Cycle Number", "1"),
        ("Visit Date", visit.visit_date.strftime(config.DATE_OUTPUT_FORMAT)),
        ("eForm Code", "frm_BloodRes"),
        ("Question Code", field_map.get(test_code)),  #type: ignore
        ("Question Cycle", data.get(config.RESULT_FIELD))
    ]))
    return ProcessedRow(init_data)

def validate_row(row:ProcessedRow)->ValidatedRow:
    """
    Validates row by checking for None values in key fields etc.
    :param row:
    :return:
    """
    for x in ["Question Code", "Visit Date", "Question Cycle"]:
        if row.get(x) is None:
            raise NotNoneableField("'" + x + "' cannot be none")

    return ValidatedRow(row)
