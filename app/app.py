'''
...\app>
python -m flask run
'''

from app.fhv import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
