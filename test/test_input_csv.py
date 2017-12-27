from pytest import fixture, mark
import sys
import csv
sys.path.extend(['/home/jan/project/movie_db'])

import helper as h
import app.import_tsv as tsv

testFile = 'test/testInput.csv'

class TestInputCsv:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(self):
        pass

    def test_openFileOk(self):
        with h.ManagedUtfFile(testFile) as f:
            csvReader = csv.reader(f)
            data = False
            for row in csvReader:
                if data == False:
                    data = True
                else:
                    items = row
                    # if len(items) > 0:
                        # print(items[0])
            assert data == True

    def test_openCsvGetTsv(self):
        with h.ManagedUtfFile(testFile) as f:
            csvReader = csv.reader(f)
            data = False
            for row in csvReader:
                if data == False:
                    data = True
                else:
                    if len(row) > 0:
                        movieId = row[0]
                        print(row, movieId)
                        imdbData = tsv.getMovieData(movieId)
                        if imdbData != None:
                            print(imdbData)
                        else:
                            print('No data found')
                        # print(imdbData)

