# MovieDB with evaluating of the favourite critics
local movie data base, based on infos from IMDB. 
Some additional informations about source, medium and rating can be added by user.
The ratings, loaded from the web-site: www.metacritics.com will be extracted and added to database.
### The main feature: based on algorithm from the book: Programming Collective Intelligence by Toby Segaran, the Pearson Similarity is calculated and the favourite critic can be evaluated

### Project serves for me as the Flask tutorial, based on Miguel Grinberg's "Flask mega tutorial" 

The user should be able to query db about the director, actor, ratings, ...

As main option user can compare her own ratings with the ratings from various critics.
Based on the ratings, the favourite critic can be evaluated

The structure of the repository:

| Name of folder | Content | Notes |
| ---- | ---- | ---- |
| venv/ | virtual interpreter | python3 |
| app | flask app | struture based on Miguel tutorial |
| imdbif | imdb data | links to files loaded from Imdb |
| db_repository | db migrations data |  |
| helper | some routines |  |
| userdata | user modified db | not under git control |
| test | pytest scripts | test should be called from parent (root) directory | 
| . | moviedb.py | main app script |
| . | find_line_tsv.py | tester for imdb tsv files script |
| . | db_*.py | helper for db migration |

### Interface to IMDB modified after changes in Dec.2017. 
Now I'm using the IMDB's TSV files downloaded, extraced and placed in imdbif folder

To extract the information from TSV file, the procedure similar to binary search was developed. 
One can check with the call:

python find_line_tsv.py -f'imdbif/title_crew.tsv' -i '0053779'  -d

