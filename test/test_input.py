from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])

import helper.helper as h

testFile = './testInput.csv'

class TestInputCsv:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(self):
        pass

    def test_openFileOk(self):
        with h.ManagedFile(testFile) as f:
            csvReader = h.inputCsvReader(f)

