import app.import_tsv as tsv

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-f", "--file", dest="filenameVariable",
                        help="write report to FILE", metavar="FILE")
    parser.add_argument("-i", "--id", dest="valueId",
                        help="ID of movie/person in IMDb", metavar="IMDBID")
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")
    # parser.add_argument("-d", "--debug",
    #                     action="store_false",
    #                     dest="debug", default=True,
    #                     help="some extra infos from function call")

    args = parser.parse_args()

    line = tsv.findLineWithId(args.filenameVariable, args.valueId)
    # line = helper.findLineWithId(file, '3397884')

    print(line)
