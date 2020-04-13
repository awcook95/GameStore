from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mangosteen@localhost/GameStore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(30), unique=True)
    pword = db.Column(db.String(100))
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)

    def __init__(self, uname, pword, name, email):
        self.uname = uname
        self.pword = pword
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Games(db.Model):
    __tablename__ = 'Games'
    gid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    publisher = db.Column(db.String(50))
    price = db.Column(db.Float)

    def __init__(self, title, platform, publisher, price):
        self.title = title
        self.platform = platform
        self.publisher = publisher
        self.price = price


class Reviews(db.Model):
    __tablename__ = 'Reviews'
    rid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    score = db.Column(db.Integer)
    body = db.Column(db.Text())

    def __init__(self, title, score, body):
        self.title = title
        self.score = score
        self.body = body


@app.route('/')
def index():
    return render_template('review.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        score = request.form['score']
        body = request.form['body']
        if title == '' or body == '':
            return render_template('review.html', message='Please enter required fields')
        data = Reviews(title, score, body)
        db.session.add(data)
        db.session.commit()
        return render_template('success.html')

if __name__ == "__main__":
    app.run()

