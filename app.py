from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mangosteen@localhost/GameStore'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:thompson@localhost:5432/New'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)



class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(30), unique=True)
    pword = db.Column(db.String(100))
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    #id = synonym('uid')
    
    def __init__(self, uname, pword, name, email):
        self.uname = uname
        self.pword = pword
        self.name = name
        self.email = email
    
    def __repr__(self):
        return '<User %r>' % self.username


class Games(db.Model):
    __tablename__ = 'games'
    gid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    publisher = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    price = db.Column(db.Float)
    
    def __init__(self, title, publisher, platform, price):
        self.title = title
        self.platform = platform
        self.publisher = publisher
        self.price = price


class Employees(db.Model):
    __tablename__ = 'employees'
    eid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(30), unique=True)
    pword = db.Column(db.String(100))
    name = db.Column(db.String(50))
    rank = db.Column(db.String(1))
    #id = synonym('eid')
    
    def __init__(self, uname, pword, name, rank):
        self.uname = uname
        self.pword = pword
        self.name = name
        self.rank = rank


class Store(db.Model):
    __tablename__ = 'store'
    sid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    
    def __init__(self, address):
        self.address = address



class Reviews(db.Model):
    __tablename__ = 'reviews'
    rid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    gid = db.Column(db.Integer)
    title = db.Column(db.String(50))
    score = db.Column(db.Integer)
    body = db.Column(db.Text())
    
    def __init__(self, uid, gid, title, score, body):
        self.uid = uid
        self.gid = gid
        self.title = title
        self.score = score
        self.body = body

class Stock(db.Model):
    __tablename__ = 'stock'
    kid = db.Column(db.Integer, primary_key=True)
    gid =  db.Column(db.Integer)
    sid = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    
    def __init__(self, gid, sid, amount):
        self.gid = gid
        self.sid = sid
        self.amount = amount



class WorksAt(db.Model):
    __tablename__ = 'worksat'
    wid = db.Column(db.Integer, primary_key=True)
    eid =  db.Column(db.Integer)
    sid = db.Column(db.Integer)
    
    def __init__(self, eid, sid):
        self.eid = gid
        self.sid = sid

class Purchase(db.Model):
    __tablename__ = 'purchase'
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    gid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    
    def __init__(self, uid, gid, sid):
        self.uid = uid
        self.gid = gid
        self.sid = sid






@app.route('/')
def login():
    return render_template('login.html')

@app.route('/try_login', methods=['GET', 'POST'])
def tryLogin():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        if uname == '' or pword == '':
            return render_template('login.html', message = "Please enter username and password")
        
        userLogin = Users.query.all()
        for user in userLogin:
             if (uname == user.uname):
                 return render_template('userMenu.html')
        
        return render_template('login.html', message = "Please enter VALID username and password")

@app.route('/user_menu', methods=['POST'])
def userMenu():
    return render_template('userMenu.html')

@app.route('/create_review', methods=['POST'])
def createReview():
    return render_template('createReview.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        title = request.form['title']
        score = request.form['score']
        body = request.form['body']
        uid = 3;
        gid = 3;
        if title == '' or body == '':
            return render_template('createReview.html', message='Please enter required fields')
        review = Reviews(uid, gid, title, score, body)
        db.session.add(review)
        db.session.commit()
        return render_template('review_success.html')

if __name__ == "__main__":
    app.run()

