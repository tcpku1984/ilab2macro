import lab2macro.data
from lab2macro import core, error, data
from typing import List,Dict,Optional, TextIO
from csv import DictWriter
import pandas as pd
import logging
from collections import OrderedDict

l = logging.getLogger("load")
import hashlib

class OutputFile:
    """
    Abstraction for CSV file output. Opens file as required and writes tests.
    """
    def __init__(self, filename:str):
        self.filename = filename
        self._file = None #type: Optional[TextIO]

    def write_tests(self, tests: lab2macro.data.ValidatedSubjectRows):
        if not self._file:
            if len(tests)==0:
                return
            logging.info("Create output file %s" % self.filename)

            self._file = open(self.filename,"w", newline='')
            self._writer = DictWriter(self._file, fieldnames = tests[0].keys())
            self._writer.writeheader()
        self._writer.writerows(tests)

    def close(self):
        if self._file:
            self._file.close()

    @property
    def checksum(self):
        h = hashlib.sha256()

        with open(str(self.filename), 'rb') as file:
            while True:
                # Reading is buffered, so we can read smaller chunks.
                chunk = file.read(h.block_size)
                if not chunk:
                    break
                h.update(chunk)

        return h.hexdigest()

def _read_csv_file(filename, delimiter=","):
    input_data = pd.read_csv(filename, sep=delimiter, na_filter=False, dtype=str)
    input_data = input_data.where((pd.notnull(input_data)), None)
    return input_data.to_dict("records")

def _process_and_write_tests(output_file:OutputFile, visit_rows:List[Dict[str,str]], input_data:List[Dict[str,str]], test_map:data.TestMap)->None:
    for visit_row in visit_rows:
        visit = core.create_subject_visit_details(visit_row) #type: core.SubjectVisitDetails

        validated_tests = core.extract_validated_visit_tests(input_data,visit,test_map) #type: core.ValidatedSubjectRows

        for e in validated_tests.errors:
            if not isinstance(e, error.NoResults):
                l.error(str(visit) + "|" + e.error_name + "|" +  str(e))

        if len(validated_tests) == 0:
            l.info("Visit " + str(visit) + " had no results")

        output_file.write_tests(validated_tests)

    output_file.close()
    logging.info("Output file closed")

def process_files(visits_filename,test_set_filename, test_data_filename, output_file:OutputFile):
    """
    Main function which reads input files and processes and writes tests
    :param visits_filename:
    :param test_set_filename:
    :param test_data_filename:
    :param output_file:
    :return:
    """
    visits = _read_csv_file(visits_filename)
    tests = _read_csv_file(test_set_filename)
    input_data = _read_csv_file(test_data_filename,'\t')

    test_map = data.TestMap(tests)

    _process_and_write_tests(output_file, visits, input_data, test_map)