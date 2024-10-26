'''
Run the following command in the root directory
python -m scripts.create_db
'''
from fhv import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
