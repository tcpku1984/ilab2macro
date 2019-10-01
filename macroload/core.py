import attr

from macroload import extract, process, config
from typing import Dict,List, Any
from collections import UserList, OrderedDict
from datetime import datetime as dt

import logging as l

@attr.s
class SubjectVisitDetails:
    """
    Represents a single visit for a subject
    """
    study_id = attr.ib() #type: str
    visit_no = attr.ib() #type: str
    visit_date = attr.ib() #type: dt.date


@attr.s
class TestInfo:
    macro_field = attr.ib() #type: str
    test_codes = attr.ib() #type: List[str]
    min = attr.ib() #type: float
    max = attr.ib() #type: float

class TestMap(OrderedDict):
    def __init__(self, tests: List[Dict[str, str]]):
        self._var_map = {}

        for test in tests:
            var_code = test['var_code']
            test_code = test['test_code']
            if var_code is None or len(var_code.strip())==0:
                raise ValueError("Variable code for test %s cannot be None/empty" % test_code)

            if test_code is None or len(test_code.strip())==0:
                raise ValueError("Test code for var %s cannot be None/empty" % var_code)

            if not self.get(var_code):
                self[var_code] = TestInfo(macro_field = var_code, test_codes=[], min = test.get("min"),max=test.get("max"))

            self[var_code].test_codes.append(test_code)
            self._var_map[test_code] = var_code

    def var_for_test(self, test_code):
        return self._var_map[test_code]

    @classmethod
    def convert_from_list(cls, tests):
        """
        Convert list of tests into test map with single key for each MACRO field
        :param tests:
        :return:
        """
        test_map = TestMap()
        for test in tests:
            var_code = test['var_code']
            test_code = test['test_code']

            if not test_map.get(var_code):
                test_map[var_code] = []

            test_map[var_code].append(test_code)

        return test_map

class ValidatedSubjectRows(UserList):
    """
    A list-like object containing validated rows and an errors property containing exceptions thrown during processing
    """
    def __init__(self, initlist, errors=[]):
        super().__init__(initlist)
        self.errors = errors
        self.unvalidated = []

class InvalidTestCode(BaseException):
    """
    Indicates a test code was not present in the test map
    """
    pass

def extract_validated_visit_tests(data:List[Dict[str,Any]], visit: SubjectVisitDetails, test_map:Dict[str, str])->ValidatedSubjectRows:
    """
    Extract and validates test rows (based on test map) from data for specific subject visit.
    :param data:
    :param visit:
    :param test_map:
    :return:
    """
    subject_tests = extract.SubjectTests.extract_for_subject(data, visit.study_id)

    validated_rows = []
    errors = []
    for macro_field, test_codes in test_map.items():
        try:
            validated_rows.append(_extract_validated_test_row(subject_tests, test_codes, test_map, visit))
        except BaseException as ex:
            errors.append(ex)

    return ValidatedSubjectRows(validated_rows,errors)

def _extract_validated_test_row(subject_tests, test_codes, test_map, visit):
    if test_codes is None or len(test_codes)==0:
        raise InvalidTestCode("Test code is None")

    dated_tests = extract.DatedSubjectSpecificTests.extract_specific_tests_with_date(subject_tests, test_codes, visit.visit_date)

    validated_rows = extract.validate_rows(dated_tests)

    processed_row = process.create_processed_row(validated_rows, visit, test_map)
    return process.validate_row(processed_row)

def create_subject_visit_details(visit_row:Dict[str,str])->SubjectVisitDetails:
    """
    Create SubjectVisitDetails instance from supplied visit data, including parsing of visit date into a datetime (using
    the config.VISIT_DATE_FORMAT property).
    :param visit_row:
    :return:
    """
    visit_date = visit_row[config.VISIT_DATE_FIELD]
    visit_no = visit_row[config.VISIT_NO_FIELD]
    study_no = visit_row[config.VISIT_STUDY_ID_FIELD]

    parsed_date = dt.strptime(visit_date, config.VISIT_DATE_FORMAT)

    return SubjectVisitDetails(study_id=study_no, visit_no=visit_no, visit_date=parsed_date)

def validate_input_data(input_data:List[Dict[str,str]]):
    """
    Validate input result data fields exist and that date format is correct
    :param input_data:
    :return:
    """
    first_row = input_data[0]
    check_fields = [config.RESULT_STUDY_ID_FIELD, config.RESULT_TEST_CODE_FIELD, config.RESULT_DATE_FIELD, config.RESULT_FIELD]

    for cf in check_fields:
        if not cf in first_row:
            raise ValueError(cf + " field is not present in input data")
    try:
        dt.strptime(first_row[config.RESULT_DATE_FIELD], config.RESULT_DATE_FORMAT)
    except BaseException:
        raise ValueError("Problem parsing result date:'" + first_row[config.RESULT_DATE_FIELD] + "' with format '" + config.RESULT_DATE_FORMAT + "'")

def validate_visit_data(visit_data:List[Dict[str,str]]):
    """
    Validate visit data fields exist and that date format is correct
    :param visit_data:
    :return:
    """
    first_row = visit_data[0]
    check_fields = [config.VISIT_STUDY_ID_FIELD, config.VISIT_DATE_FIELD, config.VISIT_NO_FIELD]

    for cf in check_fields:
        if not cf in first_row:
            raise ValueError(cf + " field is not present in input data")
    try:
        dt.strptime(first_row[config.VISIT_DATE_FIELD], config.VISIT_DATE_FORMAT)
    except BaseException:
        raise ValueError("Problem parsing visit date:" + first_row[config.VISIT_DATE_FIELD] + " with format " + config.VISIT_DATE_FORMAT)
