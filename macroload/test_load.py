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
        if len(self.rows)==0:
            raise ValueError("No rows in test file")

        headings = ",".join(self.rows[0].keys())
        rows = [",".join([str(v) for v in t.values()]) for t in self.rows]
        concat = headings + "\n" + "\n".join(rows)
        binValue = bytes(concat, "ascii")

        sha = hashlib.sha256(binValue)
        # res = base64.b64encode(sha)
        return sha.hexdigest()

def test_output_file_contents_matches_expected_crypto_hash(monkeypatch):
    #monkeypatch.setattr("macroload.config.")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_file = CheckableOutputFile(base_dir + "/test/output_file.csv")
    load.process_files(base_dir + "/test/visits.csv", base_dir + "/test/test_set.csv", base_dir + "/test/test_data.txt", output_file)
    print("cryptohash","\n".join([str(r) for r in output_file.rows]))
    assert "79682d67be278c8d32a596dd82bfbf2e1c9ca01fb1c58a5fc458979a376ec8e1" == output_file.file_cryptohash

def test_create_test_map_from_rows_handles_min_max_values_correctly():
    tests = [
        {"var_code":"Eosinophils","test_code":"EOSAB","min":"6","max":"10"},
        {"var_code": "Neutrophils", "test_code": "NEUAB", "min": "8", "max": None},
        {"var_code": "Platelets", "test_code": "PLT", "min": None, "max": "200"}
    ]
    test_map = load.create_test_map_from_rows(tests)
    assert test_map["EOSAB"] == core.TestInfo("Eosinophils",6,10)
    assert test_map["NEUAB"] == core.TestInfo("Neutrophils",8,None)
    assert test_map["PLT"] == core.TestInfo("Platelets", None, 200)
