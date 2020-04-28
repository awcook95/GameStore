from flask import Flask, render_template, request, session
from sqlalchemy.orm import sessionmaker
from collections import namedtuple
from source.models import db, Users, Games, Employees, Store, Reviews, Stock, WorksAt, Purchase
from source.gameSearch import gameSearch

app = Flask(__name__)
app.register_blueprint(gameSearch, url_prefix="/game_search")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mangosteen@localhost/GameStore'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:thompson@localhost:5432/New'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'so secret lol' #needed key for sessions to work

app.debug = True
db.init_app(app)

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

                return render_template('empMenu.html', username = session["user"], sid = session["sid"], rank = session["rank"]) #edit late to be empMenu

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

@app.route('/emp_menu', methods=['POST'])
def empMenu():
    if session["user"] == "":
        return render_template("login.html", message = "please login")
    else:
        return render_template('empMenu.html', rank = session["rank"])

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


@app.route('/about', methods = ['POST'])
def about():
    uid = session["id"]
    user = Users.query.filter(Users.uid == session["id"]).first()
    return render_template('userAboutPage.html', User = user)

@app.route('/changeUserEmail', methods = ['POST'])
def changeEmail():
    user = Users.query.filter(Users.uid == session["id"]).first()
    return render_template('userAboutPage.html', User = user, changeEmail = True)



@app.route('/changeEmailAddress', methods = ['POST'])
def changeEmailConfirm():
    user = Users.query.filter(Users.uid == session["id"]).first()
    currentpassword = request.form['currentPassword']
    newEmail = request.form['newEmailAddress']
    if(currentpassword == user.pword):
        theuser = Users.query.filter(Users.uid == session["id"]).first()
        theuser.email = newEmail
        db.session.delete(user)
        db.session.add(user)
        db.session.commit()
        return render_template('userAboutPage.html',User = user, message = "Email succesfully changed")
    else:
        return render_template('userAboutPage.html',User = user, message = "invalid password", changeEmail = True)




@app.route('/changeUserPasswordConfirm', methods = ['POST'])
def changePasswordConfirm():
    user = Users.query.filter(Users.uid == session["id"]).first()
    currentpassword = request.form['currentPassword']
    newPassword = request.form['newPassword']
    if(currentpassword == user.pword):
        theuser = Users.query.filter(Users.uid == session["id"]).first()
        theuser.pword = newPassword
        db.session.delete(user)
        db.session.add(user)
        db.session.commit()
        return render_template('userAboutPage.html',User = user, message = "Password succesfully changed")
    else:
        return render_template('userAboutPage.html',User = user, message = "invalid password", changeEmail = True)



@app.route('/changeUserPassword', methods = ['POST'])
def changePassword():
    user = Users.query.filter(Users.uid == session["id"]).first()
    return render_template('userAboutPage.html', User = user, changePassword = True)

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


@app.route('/return_games/user', methods=['POST'])
def finalizeReturn():
    username = request.form['username']
    session["currentCustomer"] = username


    uid = 0

    allUsers = Users.query.all()

    for user in allUsers:
        if(user.uname == username):
            uid = user.uid

    Game = Games.query.filter(Games.gid == session["currentGame"]).first()
    userExists = True

    if(uid == 0):
        return render_template("returnGame.html",  message = "No such username exists")




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
                currentGID = game.gid
                totalPrice+= currentPrice
                count+=1
                Stores = Store.query.all()
                for place in Stores:
                    if(place.sid == myTransaction.sid):
                        currentAddress = place.address
                        currentSID = place.sid

        aPurchase = namedtuple("aPurchase", "title price address gid sid")
        thispurchaseInfo = aPurchase(currentTitle, currentPrice, currentAddress, currentGID, currentSID)
        purchaseInfo.append(thispurchaseInfo)

    return render_template("returnGameFinal.html", listy = purchaseInfo, count = count, total = totalPrice, username = username)

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

@app.route('/store_info', methods = ['POST'])
def storeinfo():
    store = Store.query.filter(Store.sid == session["sid"]).first()
    employeeList = WorksAt.query.filter(WorksAt.sid == store.sid)
    employeesObject = []
    for emp in employeeList:
        employeesObject.append(Employees.query.filter(Employees.eid == emp.eid).order_by(Employees.rank.asc()).first())

    address = store.address

    return render_template('storeInfo.html', Employees = employeesObject, address = address)



@app.route('/check_stock', methods = ['POST'])
def checkStock():
    return render_template("checkStock.html")

@app.route('/complete_purchase', methods = ['POST'])
def purchaseSearch():
    return render_template('employeeGameSearch.html')

@app.route('/user_to_purchase',methods = ['POST'])
def userToPurchase():
    session["gameToBePurchased"] = request.form['bought']
    gid = request.form['bought']
    currentGame = Games.query.filter(Games.gid == gid).first()
    session["currentGame"] = gid
    print(gid)
    return render_template("finalizePurchase.html", game = currentGame )

@app.route('/purchase_game_withoutID', methods = ['POST'])
def removeFromStock():

    gid = session["currentGame"]
    Stocky = Stock.query.filter(Stock.gid == gid, Stock.sid == session["sid"]).first()
    Stocky.amount = Stock.amount - 1
    db.session.delete(Stocky)
    db.session.add(Stocky)
    db.session.commit()

    return render_template("empMenu.html", message = "Purchase Completed")

@app.route('/purchase_game_withID', methods = ['POST'])
def withID():
    Game = Games.query.filter(Games.gid == session["currentGame"]).first()
    userExists = True
    return render_template("finalizePurchase.html", game = Game, userExists = userExists  )

@app.route('/finalize_purchase_withID', methods = ['POST'])
def finalizeIDPurchase():
    username = request.form['username']

     #online store sid

    uid = 0

    allUsers = Users.query.all()

    for user in allUsers:
        if(user.uname == username):
            uid = user.uid

    Game = Games.query.filter(Games.gid == session["currentGame"]).first()
    userExists = True

    if(uid == 0):
        return render_template("finalizePurchase.html", game = Game, userExists = userExists, message = "No such username exists")

    sid = session["sid"]
    gid = session["currentGame"]
    Stocky = Stock.query.filter(Stock.gid == gid, Stock.sid == session["sid"]).first()
    Stocky.amount = Stock.amount - 1
    db.session.delete(Stocky)
    db.session.add(Stocky)
    db.session.commit()

    purchase = Purchase(uid, gid, sid)
    db.session.add(purchase)
    db.session.commit()


    return render_template("empMenu.html", message = "Purchase Completed")


@app.route('/check_stock/view', methods= ['POST'])
def viewStock():
    if request.method == 'POST':
        title = request.form['title']
        ListOfGames = []
        gameList = Games.query.all()
        for game in gameList:
            lowerAttribute = game.title.lower()
            lowerAttribute = lowerAttribute.strip()
            lowerAttribute = lowerAttribute.replace(" ","")

            lowerUserInput = title.lower()
            lowerUserInput = lowerUserInput.strip()
            lowerUserInput = lowerUserInput.replace(" ","")
            if(lowerUserInput in lowerAttribute):
                ListOfGames.append(game)

        size = len(ListOfGames)

        stringy = []
        stockList = Stock.query.filter(Stock.sid == session["sid"])
        #stock = Store.query.all()

        for game in ListOfGames:
            for stock in stockList:
                if(game.gid == stock.gid):
                    game.stock = stock.amount



        if(size > 0):
            return render_template("checkStockView.html", listy = ListOfGames, rank = session["rank"])
        else:
            return render_template('checkStock.html', message = 'No title By that name Found')



@app.route('/return_games', methods = ['POST'])
def returnGames():
    #session["currentUsername"] = request.form['username']
    return render_template('returnGame.html')

@app.route('/order_more', methods = ['POST'])
def orderMore():
    gid = request.form["bought"]
    sid = session["id"]

    amount = request.form["amount"]

    if(amount == "" ):
        return render_template("empMenu.html", message = "Order failed, please enter a number greater than 0 in the text field", rank = session["rank"] )

    amount = int(amount)

    if(amount < 1):
        return render_template("empMenu.html", message = "Order failed, please enter a number greater than 0 in the text field", rank = session["rank"] )


    Stocky = Stock.query.filter(Stock.gid == gid, Stock.sid == session["sid"]).first()
    Stocky.amount = Stocky.amount + amount


        #print("lol")
    db.session.delete(Stocky)
    db.session.add(Stocky)
    db.session.commit()


    return render_template("empMenu.html", message = "Order succesful", rank = session["rank"] )

@app.route('/edit_employee', methods = ['POST'])
def editEmployee():

    store = Store.query.filter(Store.sid == session["sid"]).first()
    employeeList = WorksAt.query.filter(WorksAt.sid == store.sid)
    employeesObject = []
    for emp in employeeList:
        employeesObject.append(Employees.query.filter(Employees.eid == emp.eid).order_by(Employees.rank.asc()).first())

    address = store.address

    #return render_template('storeInfo.html', Employees = employeesObject, address = address)


    return render_template("editEmployee.html", Employees = employeesObject, address = address )

@app.route('/transfer_emp', methods = ['POST'])
def transferEmployee():
    eid = request.form["transfer"]
    Employee = Employees.query.filter(Employees.eid == eid).first()

    Stores = Store.query.all()

    return render_template('transferEmployee.html', employee = Employee, stores = Stores, currentStore = session["sid"] )

@app.route('/finish_Transfer',methods = ['POST'])
def finishTransfer():
    sid = request.form['store']
    eid = request.form['eid']

    #Employee = Employees.query.filter(Employees.eid == eid).first()
    worksAt = WorksAt.query.filter(WorksAt.eid == eid, WorksAt.sid == session["sid"]).first()

    worksAt2 = worksAt
    worksAt2.sid = sid

    db.session.delete(worksAt)
    db.session.add(worksAt2)
    db.session.commit()

    return render_template("empMenu.html", rank = "M")



@app.route('/terminate_emp', methods = ['POST'])
def terminateEmployee():
    eid = request.form["terminate"]
    store = Store.query.filter(Store.sid == session["sid"]).first()
    Employee = Employees.query.filter(Employees.eid == eid).first()
    employeeList = WorksAt.query.filter(WorksAt.sid == store.sid)
    employeesObject = []
    for emp in employeeList:
        employeesObject.append(Employees.query.filter(Employees.eid == emp.eid).order_by(Employees.rank.asc()).first())

    address = store.address
    return render_template('editEmployee.html', Employees = employeesObject, employee = Employee, address = address, check = True )

@app.route('/finalize_termination', methods = ['POST'])
def finalizeTermination():
    eid = request.form['Terminate']
    sid = session["sid"]

    worksAt = WorksAt.query.filter(WorksAt.sid == sid, WorksAt.eid == eid).first()
    employee = Employees.query.filter(Employees.eid == eid).first()

    db.session.delete(worksAt)
    db.session.delete(employee)

    db.session.commit()

    return render_template("empMenu.html", rank = session["rank"])


@app.route('/complete_return', methods = ['POST'])
def completeReturn():
    username = session["currentCustomer"]
    gid = request.form['return']
    sid = request.form['return_store']
    #sid = object.sid
    #gid = object.gid
    #address = request.form['return']
    #sid = session["sid"]
    #print(address)

    User = Users.query.filter(Users.uname == username).first()

    uid = User.uid
    Game = Games.query.filter(Games.gid == gid).first()
    store =  Store.query.filter(Store.sid == sid).first()

    Stocky = Stock.query.filter(Stock.gid == gid, Stock.sid == session["sid"]).first()
    Stocky.amount = Stocky.amount + 1

    db.session.delete(Stocky)
    db.session.add(Stocky)
    print(uid, gid, sid)
    purchase = Purchase.query.filter(Purchase.gid == gid, Purchase.uid == uid, Purchase.sid == sid).first()
    #db.session.delete(purchase)



    db.session.commit()
    #print(store.address)
    #print(User.uname)
###lol



    #purchase = Purchase(uid, gid, sid)

    return render_template('empMenu.html', message = "Return Successfully Completed")



@app.route('/game_search/by_title/emp', methods= ['POST'])
def filterByTitleEmp():
    if request.method == 'POST':
        title = request.form['title']
        ListOfGames = []
        gameList = Games.query.all()
        for game in gameList:
            lowerAttribute = game.title.lower()
            lowerAttribute = lowerAttribute.strip()
            lowerAttribute = lowerAttribute.replace(" ","")

            lowerUserInput = title.lower()
            lowerUserInput = lowerUserInput.strip()
            lowerUserInput = lowerUserInput.replace(" ","")
            if(lowerUserInput in lowerAttribute):
                ListOfGames.append(game)

        size = len(ListOfGames)

        stringy = []
        stockList = Stock.query.filter(Stock.sid == session["sid"])
        #stock = Store.query.all()

        for game in ListOfGames:
            for stock in stockList:
                if(game.gid == stock.gid):
                    game.stock = stock.amount



        if(size > 0):
            return render_template("gameSearchResultsEmp.html", listy = ListOfGames)
        else:
            return render_template('employeeGameSearch.html', message = 'No title By that name Found')

@app.route('/view_reviews', methods= ['POST'])
def searchgames():
    reviewList = Reviews.query.all()
    #reviewList = db.session.query(Reviews, Users).filter(Reviews.uid == Users.uid).all()
    return render_template('viewReviews.html', reviewList = reviewList)



if __name__ == "__main__":
    app.run()
