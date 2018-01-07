import app.mod_imdb.controllers as tsv


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-f", "--file", dest="filenameVariable",
                        help="write report to FILE", metavar="FILE")
    parser.add_argument("-i", "--id", dest="valueId",
                        help="ID of movie/person in IMDb", metavar="IMDBID")
    # defalt True enable changeing, with default=False nothing changes
    parser.add_argument("-d", "--debug",
                        action="store_false", dest="quiet", default=True,
                        help="don't print status messages to stdout")

    args = parser.parse_args()

    print(args.filenameVariable)
    print('quiet = {}'.format(args.quiet))

    line = tsv.findLineWithId(args.filenameVariable, args.valueId, quiet=args.quiet)

    print(line)
