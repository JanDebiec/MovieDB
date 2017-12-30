# MovieDB
local movie data base, based on infos from IMDB. 
Some additional informations about source, medium and rating can be added by user

The user should be able to query db about the director, actor, ratings, ...

As option user can compare her own ratings with the ratings from various critics and sites

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


