
from lab2macro import load,core, data
from typing import List
import hashlib
import os, sys
class CheckableOutputFile(load.OutputFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.rows = [] #type: List[core.ValidatedSubjectRows]


    def write_tests(self, tests: data.ValidatedSubjectRows):
        self.rows = self.rows + list(tests)

    @property
    def checksum(self):
        if len(self.rows)==0:
            raise ValueError("No rows in test file")

        headings = ",".join(self.rows[0].keys())
        rows = [",".join([str(v) for v in t.values()]) for t in self.rows]
        concat = headings + "\n" + "\n".join(rows)
        binValue = bytes(concat, "ascii")

        sha = hashlib.sha256(binValue)
        # res = base64.b64encode(sha)
        return sha.hexdigest()

def test_internal_output_file_contents_matches_expected_checksum():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_file = CheckableOutputFile(base_dir + "/test/output_file.csv")
    load.process_files(base_dir + "/test/visits.csv", base_dir + "/test/test_set.csv", base_dir + "/test/test_data.txt", output_file)
    assert "a0e393e76a78b719d80c732996d46225feea8fa08dda2c2b65fcfa9969439093" == output_file.checksum

def test_real_output_file_matches_checksum():
    import os

    base_dir = os.path.abspath(os.path.dirname(__file__))

    output_file = load.OutputFile(base_dir + "/test/output_file.csv")

    try:
        os.unlink(output_file.filename)
    except FileNotFoundError:
        pass

    load.process_files(base_dir + "/test/visits.csv", base_dir + "/test/test_set.csv", base_dir + "/test/test_data.txt",output_file)
    assert "ab678f592032e3b872191fc1e4b822c0f650c0b12b962f483f43d503b1ea4095" == output_file.checksum
