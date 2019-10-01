from collections import OrderedDict, UserList
from typing import List, Dict, Optional
import datetime as dt
import attr


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
    min = attr.ib() #type: Optional[float]
    max = attr.ib() #type: Optional[float]


class TestMap(OrderedDict):
    """
    Convert list of tests into test map with single key for each MACRO field
    :param tests:
    :return:
    """
    def __init__(self, tests: List[Dict[str, str]]):
        self._var_map = {} #type: Dict[str,str]

        for test in tests:
            var_code = test['var_code']
            test_code = test['test_code']
            if var_code is None or len(var_code.strip())==0:
                raise ValueError("Variable code for test %s cannot be None/empty" % test_code)

            if test_code is None or len(test_code.strip())==0:
                raise ValueError("Test code for var %s cannot be None/empty" % var_code)

            if not self.get(var_code):
                str_min = test.get("min")
                str_max = test.get("max")

                min = float(str_min) if str_min else None

                max = float(str_max) if str_max else None

                self[var_code] = TestInfo(macro_field = var_code, test_codes=[], min = min, max=max)

            self[var_code].test_codes.append(test_code)
            self._var_map[test_code] = var_code

    def info_for_test_code(self, test_code):
        return self.get(self._var_map[test_code])

class ValidatedSubjectRows(UserList):
    """
    A list-like object containing validated rows and an errors property containing exceptions thrown during processing
    """
    def __init__(self, initlist, errors=[]):
        super().__init__(initlist)
        self.errors = errors
        self.unvalidated = []