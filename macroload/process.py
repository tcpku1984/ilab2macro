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


def create_processed_row(data:extract.BaseValidatedTest, visit: "core.SubjectVisitDetails", test_info: "core.TestInfo")->ProcessedRow:
    """
    Creates processed row by amalgamating the visit info, the validated test and the config.COMMON_OUTPUT_VALUES
    :param data:
    :param visit:
    :param test_map:
    :return:
    """
    init_data = config.INITIAL_ROW.copy()
    test_code = data.test_code
    init_data.update({
        "Subject Label": visit.study_id,
        "Visit Code": visit.visit_no,
        "Visit Date": visit.visit_date.strftime(config.DATE_OUTPUT_FORMAT),
        "Question Code": test_info.macro_field,
        "Question Value": data.result,
        "Unobtainable status":data.unobtainable_status
    })
    return ProcessedRow(init_data)

def validate_required_fields(row:ProcessedRow)->ValidatedRow:
    """
    Validates row by checking for None values in key fields etc.
    :param row:
    :return:
    """
    for x in ["Question Code", "Visit Date", "Question Cycle","Question Value","Subject ID","Visit Code"]:
        if row.get(x) is None:
            raise NotNoneableField("'" + x + "' cannot be none")

    return ValidatedRow(row)
