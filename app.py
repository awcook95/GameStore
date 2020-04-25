from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from collections import namedtuple

from source.gameSearch import gameSearch

app = Flask(__name__)
app.register_blueprint(gameSearch, url_prefix="/game_search")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mangosteen@localhost/GameStore'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:thompson@localhost:5432/New'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'so secret lol' #needed key for sessions to work

app.debug = True
db = SQLAlchemy(app)


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




@app.route('/')
def login():
    return render_template('login.html')

@app.route('/try_login', methods=[ 'POST'])
def tryLogin():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        if uname == '' or pword == '':
            return render_template('login.html', message = "Please enter username and password")

        userLogin = Users.query.all()
        for user in userLogin:
             if (uname == user.uname and pword == user.pword):
                 session["user"] = uname
                 session["id"] = user.uid
                 return render_template('userMenu.html', username = session["user"], uid = session["id"])

        employeeLogin = Employees.query.all()
        for emp in employeeLogin:
            if(uname == emp.uname and pword == emp.pword):
                session["user"] = uname
                session["id"] = emp.eid
                session["rank"] = emp.rank

                store = WorksAt.query.filter(WorksAt.eid == emp.eid).first()
                session["sid"] = store.sid


                return render_template('empMenu.html', username = session["user"], sid = session["sid"]) #edit late to be empMenu

        return render_template('login.html', message = "Please enter VALID username and password")


@app.route('/logout', methods =['POST'])
def logout():

    session["user"] = ""
    session["id"] = ""
    session["rank"] = ""
    return render_template('login.html', message = "succesfully logged out")


@app.route('/user_menu', methods=['POST'])
def userMenu():
    if session["user"] == "":
        return render_template("login.html", message = "please login")
    else:
        return render_template('userMenu.html')




@app.route('/find_store', methods=['POST'])
def findStore():
    option = request.form['option']
    if option == '':
        return render_template('findStore.html')
    elif option == 'all':
        stores = Store.query.all()
        return render_template('findStore.html', stores=stores)
    else:
        state = option
        stores = Store.query.filter(Store.address.match(f'%{state}%')).all()
        return render_template('findStore.html', stores=stores)








@app.route('/purchase_game', methods = ['POST'])
def orderGame():
    uid = session["id"]
    gid = request.form['bought']
    sid = 6 #online store sid
    purchase = Purchase(uid, gid, sid)
    db.session.add(purchase)
    db.session.commit()
    return render_template('userMenu.html')




@app.route('/view_orders', methods=['POST'])
def viewOrders():
    uid = session["id"]
    listOfPurchases = []
    #Purchases = Purchase.query.all()
    #Purchases = Purchase.query.order_by(Purchase.date.desc())
    Purchases = Purchase.query.order_by(Purchase.gid.desc()) #NEED TO orderbyDatePurchased probably
    for transaction in Purchases:
        if(transaction.uid == uid):
            listOfPurchases.append(transaction)


    purchaseInfo = []


    totalPrice = 0
    count = 0
    for myTransaction in listOfPurchases:
        gameList = Games.query.all()
        for game in gameList:
            if(game.gid == myTransaction.gid):
                currentTitle = game.title
                currentPrice = game.price
                totalPrice+= currentPrice
                count+=1
                Stores = Store.query.all()
                for place in Stores:
                    if(place.sid == myTransaction.sid):
                        currentAddress = place.address



        aPurchase = namedtuple("aPurchase", "title price address")
        thispurchaseInfo = aPurchase(currentTitle, currentPrice, currentAddress)
        purchaseInfo.append(thispurchaseInfo)

    return render_template("userOrders.html", listy = purchaseInfo, count = count, total = totalPrice)





@app.route('/create_review', methods=['POST'])
def createReview():
    return render_template('createReview.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        title = request.form['title']
        score = request.form['score']
        body = request.form['body']
        uid = session["id"]
        if title == '' or body == '':
            return render_template('createReview.html', message='Please enter required fields')

        confirmTitle = 'invalid'
        gameTitle = Games.query.all()
        for game in gameTitle:
            if(game.title == title):
                confirmTitle = title
                gid = game.gid
        if(confirmTitle == 'invalid'):
                return render_template('createReview.html', message= 'Game does not exist in our records')
        review = Reviews(uid, gid, title, score, body)
        db.session.add(review)
        db.session.commit()
        return render_template('review_success.html')

if __name__ == "__main__":
    app.run()
