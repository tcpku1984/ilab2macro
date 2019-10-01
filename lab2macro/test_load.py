import lab2macro.data
from lab2macro import load,core
from typing import List,Dict
import hashlib
import os, sys
class CheckableOutputFile(load.OutputFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.rows = [] #type: List[core.ValidatedSubjectRows]


    def write_tests(self, tests: lab2macro.data.ValidatedSubjectRows):
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

def test_output_file_contents_matches_expected_checksum(monkeypatch):
    #monkeypatch.setattr("lab2macro.config.")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_file = CheckableOutputFile(base_dir + "/test/output_file.csv")
    load.process_files(base_dir + "/test/visits.csv", base_dir + "/test/test_set.csv", base_dir + "/test/test_data.txt", output_file)
    print("cryptohash","\n".join([str(r) for r in output_file.rows]))
    assert "e7552eb509506ce36b967d1888e2831a8e0c7d0ee2e449c110a21f6f97be0d57" == output_file.checksum

