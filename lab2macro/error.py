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


class NotNoneableField(RowValidationError):
    """
    Raised when required field has None value
    """
    pass


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