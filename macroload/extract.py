import datetime as dt
from typing import List, Dict
from collections import UserList, OrderedDict
from macroload import config

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
    def __init__(self, initlist, subject_id, date, test_codes):
        super().__init__(initlist)
        self.subject_id = subject_id
        self.date = date
        self.test_codes = test_codes

    @staticmethod
    def extract_specific_tests_with_date(data: SubjectTests, test_codes, search_date: dt.date) -> "DatedSubjectSpecificTests":
        """
        Parse date and then extract rows matching a specific search_date
        :param data:
        :param search_date:
        :return:
        """
        test_data = list(filter(lambda x: x[config.RESULT_TEST_CODE_FIELD] in test_codes, data))
        search_date_str = search_date.strftime(config.DATE_OUTPUT_FORMAT)
        parsed_row = [_parse_date_field(row) for row in test_data]
        dated_rows = list(filter(lambda x: x[config.PARSED_RESULT_DATE_FIELD] == search_date_str, parsed_row))
        return DatedSubjectSpecificTests(dated_rows, data.subject_id, search_date, test_codes)


class BaseValidatedTest:
    """
    Base class for a validated test, the derived class is either ValidatedResultTest or ValidatedEmptyTest
    """
    def __init__(self, data:DatedSubjectSpecificTests):
        self.subject_id = data.subject_id
        self.test_date = data.date

    @property
    def result(self):
        raise NotImplementedError()

    @property
    def unobtainable_status(self):
        raise NotImplementedError()


    result = None

class ValidatedResultTest(BaseValidatedTest):
    """
    A single validated result for a specific test and subject for a specific date
    """

    def __init__(self, data:DatedSubjectSpecificTests):
        self._result = data[0][config.RESULT_FIELD]
        self.test_code = data[0][config.RESULT_TEST_CODE_FIELD]

        super().__init__(data)

    @property
    def result(self):
        return self._result

    @property
    def unobtainable_status(self):
        return ""

class ValidatedUnobtainableTest(BaseValidatedTest):
    """
    A single unobtainable result for a specific test and subject for a specific date
    """

    def __init__(self, data:DatedSubjectSpecificTests):
        self.test_code = data.test_codes[0]
        super().__init__(data)

    @property
    def result(self):
        return ""

    @property
    def unobtainable_status(self):
        return "1"


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


def validate_rows(data:DatedSubjectSpecificTests)->BaseValidatedTest:
    """
    Validate the row by raising exceptions for inconsistent and/or empty results. If it is successful it returns a single validated test
    :param data:
    :return:
    """
    results = {}
    for row in data:
        results[row[config.RESULT_FIELD]] = True

    if len(results.items())>1:
        data = {
            "date_time":[i[config.RESULT_DATE_FIELD] for i in data],
            "test":[i[config.RESULT_TEST_CODE_FIELD] for i in data],
            "study_id":[i[config.RESULT_STUDY_ID_FIELD] for i in data],
            "result":[i[config.RESULT_FIELD] for i in data]
        }
        raise InconsistentResults("Inconsistent results in:" + str(data))

    if len(results.items())==0:
        return ValidatedUnobtainableTest(data)

    _guard_against_invalid_number(row[config.RESULT_FIELD], test_info.min, test_info.max)

    return ValidatedResultTest(row)

def _parse_date_field(row:Dict[str,str])->Dict[str,str]:
    parsed_date = dt.datetime.strptime(row[config.RESULT_DATE_FIELD], config.RESULT_DATE_FORMAT)
    new_row = row.copy()
    new_row[config.PARSED_RESULT_DATE_FIELD] = parsed_date.strftime(config.DATE_OUTPUT_FORMAT)
    return new_row

def _guard_against_invalid_number(result:str, min:Optional[float], max:Optional[float]):
    if result is None:
        raise error.NonNumericResult("Result is None")

    result = str(result)

    if result.startswith(">") or result.startswith("<"):
        result = result[1:]
    try:
        num_result = float(result)

        print("min:%s, max:%s, result:%s" % (min,max, num_result))
        if min and num_result<min:
            raise error.NumberOutOfRange("Result %s less than minimum (%s)" % (num_result, min))

        if max and num_result>max:
            raise error.NumberOutOfRange("Result %s more than maximum (%s)" % (num_result, max))

    except ValueError:
        raise error.NonNumericResult("Result %s is not numeric" % result)
