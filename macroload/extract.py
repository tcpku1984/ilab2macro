import datetime as dt
from typing import List, Dict
from collections import UserList, OrderedDict
from macroload import config, core

class SubjectTests(UserList):
    """
    All tests for a subject
    """
    pass

class SubjectSpecificTests(UserList):
    """
    All results for a specific test and subject
    """
    pass

class ParsedSubjectSpecificTests(UserList):
    """
    All results for a specific test and subject which have had their test date parsed
    """
    pass

class DatedSubjectSpecificTests(UserList):
    """
    All results for a specific test and subject for a specific date
    """
    pass

class ValidatedSubjectSpecificTest(OrderedDict):
    """
    A single validated result for a specific test and subject for a specific date
    """
    pass

class InconsistentResults(BaseException):
    """
    Raised when two or more results of the same subject, date and test type do not match
    """
    pass

class NoResults(BaseException):
    """
    Raised when no results for the subject, date and test type
    """
    pass

def extract_subject_tests(data:List[Dict[str,str]], subject_id:str)->SubjectTests:
    """
    Extract all rows which match the supplied subject ID
    :param data:
    :param subject_id:
    :return:
    """
    return SubjectTests(list(filter(lambda x: x.get(config.STUDY_ID_FIELD) == subject_id, data)))

def parse_subject_tests_date(data:SubjectSpecificTests)->ParsedSubjectSpecificTests:
    """
    Parse the test date according to the config.RESULT_DATE_FORMAT into the output format config.DATE_OUTPUT_FORMAT
    :param data:
    :return:
    """
    return ParsedSubjectSpecificTests([_parse_date_field(row) for row in data])

def extract_rows_with_date(data:ParsedSubjectSpecificTests, search_date:dt.date)->DatedSubjectSpecificTests:
    """
    Extract rows matching a specific search_date
    :param data:
    :param search_date:
    :return:
    """
    search_date_str = search_date.strftime(config.DATE_OUTPUT_FORMAT)
    return DatedSubjectSpecificTests(list(filter(lambda x: x.get(config.DATE_FIELD) == search_date_str, data)))

def extract_specific_tests(data:SubjectTests, test_code:str)->SubjectSpecificTests:
    """
    Extract specific tests with the supplied test_code
    :param data:
    :param test_code:
    :return:
    """
    filt = filter(lambda x: x[config.TEST_CODE_FIELD] == test_code, data)
    return SubjectSpecificTests(list(filt))

def validate_rows(data:DatedSubjectSpecificTests)->ValidatedSubjectSpecificTest:
    """
    Validate the row by raising exceptions for inconsistent and/or empty results. If it is successful it returns a single validated test
    :param data:
    :return:
    """
    results = {}
    for row in data:
        results[row[config.RESULT_FIELD]] = True

    if len(results.items())>1:
        raise InconsistentResults("In result:" + str(data))

    if len(results.items())==0:
        raise NoResults()

    return ValidatedSubjectSpecificTest(data[0])

def _parse_date_field(row:Dict[str,str])->Dict[str,str]:
    parsed_date = dt.datetime.strptime(row[config.DATE_FIELD], config.RESULT_DATE_FORMAT)
    new_row = row.copy()
    new_row[config.DATE_FIELD] = parsed_date.strftime(config.DATE_OUTPUT_FORMAT)
    return new_row