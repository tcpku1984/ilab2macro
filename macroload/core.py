from collections import namedtuple
import attr

from macroload import extract, process, config
from typing import Dict,List, Any, NamedTuple, TextIO, Optional
from collections import UserList
import datetime as dt

import logging as l
import pandas as pd

l.basicConfig(level = l.INFO)

@attr.s
class SubjectVisitDetails:
    """
    Represents a single visit for a subject
    """
    study_id = attr.ib() #type: str
    visit_no = attr.ib() #type: str
    visit_date = attr.ib() #type: dt.date

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
    subject_tests = extract.extract_subject_tests(data, visit.study_id)

    validated_rows = []
    errors = []
    for test_code, macro_field in test_map.items():
        try:
            validated_rows.append(_extract_validated_test_rows(subject_tests, test_code, test_map, visit))
        except BaseException as ex:
            errors.append(ex)

    return ValidatedSubjectRows(validated_rows,errors)

def _extract_validated_test_rows(subject_tests, test_code, test_map, visit):
    if test_code is None:
        raise InvalidTestCode("Test code is None")

    specific_tests = extract.extract_specific_tests(subject_tests, test_code)
    parsed_tests = extract.parse_subject_tests_date(specific_tests)
    dated_tests = extract.extract_rows_with_date(parsed_tests, visit.visit_date)

    try:
        validated_rows = extract.validate_rows(dated_tests)
    except extract.NoResults:
        raise extract.NoResults("Unable to find results for test code:" + str(test_code))

    processed_row = process.create_processed_row(validated_rows, visit, test_map)
    return process.validate_row(processed_row)

def create_subject_visit_details(visit_row:Dict[str,str])->SubjectVisitDetails:
    """
    Create SubjectVisitDetails instance from supplied visit data, including parsing of visit date into a datetime (using
    the config.VISIT_DATE_FORMAT property).
    :param visit_row:
    :return:
    """
    visit_date = visit_row['Visit date']
    visit_no = visit_row['Visit number']
    study_no = visit_row['Screening Number']

    parsed_date = dt.datetime.strptime(visit_date, config.VISIT_DATE_FORMAT)

    if parsed_date is None:
        raise ValueError("Visit date " + str(visit_date) + " could not be parsed")

    return SubjectVisitDetails(study_id=study_no, visit_no=visit_no, visit_date=parsed_date)

