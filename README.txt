This is a simple webapp that allows users to login
and view games as well as read/create game reviews

Make sure you have python installed, if you don't already

to create database tables in postgresql:
create new databse with pgadmin
use command "python" to enter python shell
The shell will allow you to run lines of python code
Use commands:
    from app import db
    db.create_all()
This will create the tables specified in app.py

To run, use commands:
    pip install pipenv #if you have not installed pipenv, do it now
    pipenv shell #creates a virtual environment in the current directory
    pipenv sync #this will install all packages listed in pipfile, pipenv install works too but it will get the latest version
    python app.py #host app

