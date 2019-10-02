from lab2macro import config, core, result, data

from collections import OrderedDict
from lab2macro.error import RequiredField


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


def create_processed_row(data: result.BaseValidatedResult, visit: "core.SubjectVisitDetails", test_info: "data.TestInfo")->ProcessedRow:
    """
    Creates processed row by amalgamating the visit info, the validated test and the config.INITIAL_ROW
    :param data:
    :param visit:
    :param test_map:
    :return:
    """
    init_data = config.INITIAL_ROW.copy()
    init_data.update({
        "Subject Label": visit.study_id,
        "Visit Code": visit.visit_no,
        "Visit Date": visit.visit_date.strftime(config.OUTPUT_DATE_FORMAT),
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
            raise RequiredField(x)

    return ValidatedRow(row)
