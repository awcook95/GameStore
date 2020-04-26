from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
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


class Purchase(db.Model): #need to Add datePurchased
    __tablename__ = 'purchase'
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    gid = db.Column(db.Integer)
    sid = db.Column(db.Integer)

    def __init__(self, uid, gid, sid):
        self.uid = uid
        self.gid = gid
        self.sid = sid