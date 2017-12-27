import helper
from argparse import ArgumentParser

file = 'imdbif/title_crew.tsv'
# file = 'imdbif/title_basics.tsv'





parser = ArgumentParser()

# Add more options if you like
parser.add_argument("-f", "--file", dest="filenameVariable",
                    help="write report to FILE", metavar="FILE")
parser.add_argument("-i", "--id", dest="valueId",
                    help="ID of movie/person in IMDb", metavar="IMDBID")
parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

args = parser.parse_args()

print(args.filenameVariable)
print(args.filenameVariable)

# line = helper.findLineWithId(args.filenameVariable, args.valueId)
line = helper.findLineWithId(file, '3397884')

print(line)
