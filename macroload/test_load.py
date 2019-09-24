from macroload import load,core
from typing import List,Dict
import hashlib
import os, sys
class CheckableOutputFile(load.OutputFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.rows = [] #type: List[core.ValidatedSubjectRows]


    def write_tests(self, tests:core.ValidatedSubjectRows):
        self.rows = self.rows + list(tests)

    @property
    def file_cryptohash(self):
        headings = ",".join(self.rows[0].keys())
        rows = [",".join([str(v) for v in t.values()]) for t in self.rows]
        concat = headings + "\n" + "\n".join(rows)
        binValue = bytes(concat, "ascii")

        sha = hashlib.sha256(binValue)
        # res = base64.b64encode(sha)
        return sha.hexdigest()

def test_output_file_contents_matches_expected_crypto_hash():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_file = CheckableOutputFile(base_dir + "/test/output_file.csv")
    load.process_files(base_dir + "/test/visits.csv", base_dir + "/test/test_set.csv", base_dir + "/test/test_data.csv", output_file)
    assert "79682d67be278c8d32a596dd82bfbf2e1c9ca01fb1c58a5fc458979a376ec8e1" == output_file.file_cryptohash

