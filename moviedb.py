#!flask/bin/python
from app import create_app, db
from app.mod_db.models import  Movie, People, Director, Role

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db , 'Movie':Movie, 'People':People, 'Director':Director, 'Role':Role}

# app will be started from "flask run"
# app.run(debug=True)
