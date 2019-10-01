from lab2macro import config, extract
from abc import abstractmethod
class BaseValidatedResult:
    """
    Base class for a validated test, the derived class is either ValidatedResultTest or ValidatedEmptyTest
    """
    def __init__(self, data:"extract.DatedSubjectSpecificTests"):
        self.subject_id = data.subject_id
        self.test_date = data.date

    @property
    @abstractmethod
    def result(self):
        raise NotImplementedError()

    @property
    def unobtainable_status(self):
        raise NotImplementedError()


class ValidatedResult(BaseValidatedResult):
    """
    A single validated result for a specific test and subject for a specific date
    """

    def __init__(self, data:"extract.DatedSubjectSpecificTests"):
        self._result = data[0][config.RESULT_FIELD]
        self.test_code = data[0][config.RESULT_TEST_CODE_FIELD]

        super().__init__(data)

    @property
    def result(self):
        return self._result

    @property
    def unobtainable_status(self):
        return ""


class ValidatedUnobtainableTest(BaseValidatedResult):
    """
    A single unobtainable result for a specific test and subject for a specific date
    """

    def __init__(self, data:"extract.DatedSubjectSpecificTests"):
        self.test_code = data.test_info.test_codes[0]
        super().__init__(data)

    @property
    def result(self):
        return ""

    @property
    def unobtainable_status(self):
        return "1"