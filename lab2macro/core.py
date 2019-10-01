from lab2macro import extract, process, config, data
from typing import Dict,List, Any
from datetime import datetime as dt

from lab2macro.data import SubjectVisitDetails, ValidatedSubjectRows

def extract_validated_visit_tests(data:List[Dict[str,Any]], visit: SubjectVisitDetails, test_map:data.TestMap)-> ValidatedSubjectRows:
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
    for macro_field, test_info in test_map.items():
        try:
            validated_rows.append(
                _extract_validated_test_row(subject_tests, test_info, visit)
            )
        except BaseException as ex:
            errors.append(ex)

    return ValidatedSubjectRows(validated_rows, errors)

def _extract_validated_test_row(subject_tests, test_info: data.TestInfo, visit):
    dated_tests = extract.DatedSubjectSpecificTests.extract_specific_tests_with_date(subject_tests, test_info, visit.visit_date)

    validated_rows = extract.validate_rows(dated_tests)

    processed_row = process.create_processed_row(validated_rows, visit, test_info)
    return process.validate_required_fields(processed_row)

def create_subject_visit_details(visit_row:Dict[str,str])-> SubjectVisitDetails:
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
