from lab2macro import config
class TestError(BaseException):
    def __init__(self, error:BaseException, data):
        self.error = error

        ex_data = {
            "date_time": [i[config.RESULT_DATE_FIELD] for i in data],
            "test": [i[config.RESULT_TEST_CODE_FIELD] for i in data],
            "study_id": [i[config.RESULT_STUDY_ID_FIELD] for i in data],
            "result": [i[config.RESULT_FIELD] for i in data]
        }

        self.data = ex_data

    @property
    def error_name(self):
        return self.error.__class__.__name__

    def __repr__(self):
        return "%s (data:%s)" % (str(self.error), str(self.data))

    def __str__(self):
        return self.__repr__()

class RowValidationError(BaseException):
    pass

class InconsistentResults(RowValidationError):
    """
    Raised when two or more results of the same subject, date and test type do not match
    """
    pass


class NoResults(RowValidationError):
    """
    Raised when no results for the subject, date and test type
    """
    pass


class NonNumericResult(RowValidationError):
    """
    Raised when not numeric or prefixed numeric test
    """
    pass


class RequiredField(RowValidationError):
    """
    Raised when required field has None value
    """
    def __init__(self, field_name):
        super().__init__(field_name + " is required")


class InvalidTestCode(RowValidationError):
    """
    Indicates a test code was not present in the test map
    """
    pass

class NumberOutOfRange(RowValidationError):
    """
    Raised when a number is less than minimum or more than minimum allowed result.
    """
    pass