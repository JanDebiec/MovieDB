import csv
import helper as h


def repairIdInCsv(fileName):
    fileNameWrite = fileName + 'backup'
    new_rows_list = []
    with h.ManagedUtfFile(fileName) as f:
        csvReader = csv.reader(f)
        count = 0
        data = False
        for row in csvReader:
            if data == False:
                new_rows_list.append(row)
                data = True
            else:
                if len(row) > 0:
                    count = count + 1
                    imdbIDOld = row[0]
                    length = len(imdbIDOld)
                    if length < 7:
                        imdbINew = ("0" * (7 - length)) + imdbIDOld
                    else:
                        imdbINew = imdbIDOld
                    newrow = [imdbINew,]
                    newrow.extend(row[1:])
                    print(newrow)
                    new_rows_list.append(newrow)

    with h.ManagedUtfFile(fileName, mode='w') as fw:

        # file2 = open(file.csv, 'wb')
        writer = csv.writer(fw)
        writer.writerows(new_rows_list)
        # file2.close()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-f", "--file", dest="filenameVariable",
                        help="write report to FILE", metavar="FILE")
    # defalt True enable changeing, with default=False nothing changes
    parser.add_argument("-d", "--debug",
                        action="store_false", dest="quiet", default=True,
                        help="don't print status messages to stdout")

    args = parser.parse_args()

    print(args.filenameVariable)
    print('quiet = {}'.format(args.quiet))

    repairIdInCsv(args.filenameVariable)


