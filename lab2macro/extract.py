import datetime as dt
from typing import List, Dict, Optional, Tuple
from collections import UserList
from lab2macro.data import TestInfo

from lab2macro import config, error
from lab2macro.result import BaseValidatedResult, ValidatedResult, ValidatedUnobtainableTest

class SubjectTests(UserList):
    """
    All tests for a subject
    """
    def __init__(self, initlist:List, subject_id:str):
        super().__init__(initlist)
        self.subject_id = subject_id

    @staticmethod
    def extract_for_subject(data, subject_id:str)->"SubjectTests":
        """
        Extract all rows which match the supplied subject ID
        :param data:
        :param subject_id:
        :return:
        """
        return SubjectTests(list(filter(lambda x: x[config.RESULT_STUDY_ID_FIELD] == subject_id, data)), subject_id)


class DatedSubjectSpecificTests(UserList):
    """
    All results for a specific test and subject for a specific date
    """
    def __init__(self, initlist:List[Dict[str,str]], subject_id:str, date: dt.date, test_info: TestInfo):
        super().__init__(initlist)
        self.subject_id = subject_id
        self.date = date
        self.test_info = test_info

    @staticmethod
    def extract_specific_tests_with_date(data: SubjectTests, test_info:TestInfo, search_date: dt.date) -> "DatedSubjectSpecificTests":
        """
        Parse date and then extract rows matching a specific search_date
        :param data:
        :param search_date:
        :return:
        """
        test_data = list(filter(lambda x: x[config.RESULT_TEST_CODE_FIELD] in test_info.test_codes, data))
        search_date_str = search_date.strftime(config.OUTPUT_DATE_FORMAT)
        parsed_row = [_parse_date_field(row) for row in test_data]
        dated_rows = list(filter(lambda x: x[config.RESULT_PARSED_DATE_FIELD] == search_date_str, parsed_row))
        return DatedSubjectSpecificTests(dated_rows, data.subject_id, search_date, test_info)


def validate_rows(data:DatedSubjectSpecificTests)-> BaseValidatedResult:
    """
    Validate the row by raising exceptions for inconsistent and/or empty results. If it is successful it returns a single validated test
    :param data:
    :return:
    """

    clean_data, num_string_results = _remove_string_data(data)

    results = {}

    for row in clean_data:
        results[row[config.RESULT_FIELD]] = True

    if len(results.items()) == 0:
       if num_string_results > len(results):
           raise error.NonNumericResult()
       else:
           return ValidatedUnobtainableTest(data)

    if len(results.items()) > 1:
            raise error.InconsistentResults()

    _guard_against_invalid_number(clean_data[0][config.RESULT_FIELD], clean_data.test_info.min, clean_data.test_info.max)

    return ValidatedResult(clean_data)

def _parse_date_field(row:Dict[str,str])->Dict[str,str]:
    parsed_date = dt.datetime.strptime(row[config.RESULT_DATE_FIELD], config.RESULT_DATE_FORMAT)
    new_row = row.copy()
    new_row[config.RESULT_PARSED_DATE_FIELD] = parsed_date.strftime(config.OUTPUT_DATE_FORMAT)
    return new_row

def _remove_string_data(data:DatedSubjectSpecificTests)->Tuple[DatedSubjectSpecificTests,int]:
    clean_data = []

    num_strings = 0
    for item in data:
        result = str(item[config.RESULT_FIELD])

        if result.startswith(">") or result.startswith("<"):
            result = result[1:]

        try:
            float(result)
            clean_data.append(item)
        except ValueError:
            num_strings+=1

    return DatedSubjectSpecificTests(clean_data,data.subject_id, data.date, data.test_info)  , num_strings

def _guard_against_invalid_number(result:str, min:Optional[float], max:Optional[float]):
    if result is None:
        raise error.NonNumericResult("Result is None")

    result = str(result)

    if result.startswith(">") or result.startswith("<"):
        result = result[1:]

    num_result = float(result)

    if min and num_result<min:
        raise error.NumberOutOfRange("Result %s less than minimum (%s)" % (num_result, min))

    if max and num_result>max:
        raise error.NumberOutOfRange("Result %s more than maximum (%s)" % (num_result, max))

