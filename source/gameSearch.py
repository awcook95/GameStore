from flask import Blueprint, render_template, request
from source.models import Games

gameSearch = Blueprint("gameSearch", __name__, static_folder='static', static_url_path='../static', template_folder='templates')

@gameSearch.route('', methods= ['POST'])
def searchgames():
    return render_template('gameSearch.html')


@gameSearch.route('/all', methods= ['POST'])
def filterByAll():
    if request.method == 'POST':
        gameList = Games.query.all()
        ListOfGames = []
        for game in gameList:
                ListOfGames.append(game)

        size = len(ListOfGames)
        if(size > 0):
            return render_template("gameSearchResults.html", listy = ListOfGames)
        else:
            return render_template('gameSearch.html', message = 'No games By that platform Found')


@gameSearch.route('/by_title', methods= ['POST'])
def filterByTitle():
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

        for game in ListOfGames:
            stringy.append(game.title)
            print(game.title)

        if(size > 0):
            return render_template("gameSearchResults.html", listy = ListOfGames)
        else:
            return render_template('gameSearch.html', message = 'No title By that name Found')


@gameSearch.route('/by_publisher', methods= ['POST'])
def filterByPublisher():
    if request.method == 'POST':
        publisher = request.form['publisher']
        ListOfGames = []
        publisherList = Games.query.all()
        for game in publisherList:
            lowerAttribute = game.publisher.lower()
            lowerAttribute = lowerAttribute.strip()
            lowerAttribute = lowerAttribute.replace(" ","")

            lowerUserInput = publisher.lower()
            lowerUserInput = lowerUserInput.strip()
            lowerUserInput = lowerUserInput.replace(" ","")
            if(lowerUserInput in lowerAttribute):
                ListOfGames.append(game)

        if(len(ListOfGames) > 0):
            return render_template("gameSearchResults.html", listy = ListOfGames)
        else:
            return render_template('gameSearch.html', message = 'No publisher By that name Found')

@gameSearch.route('/by_platform', methods= ['POST'])
def filterByPlatform():
    if request.method == 'POST':
        platform = request.form['platform']
        gameList = Games.query.all()
        ListOfGames = []
        for game in gameList:
            if(game.platform.lower() == platform.lower()):
                ListOfGames.append(game)

        size = len(ListOfGames)
        if(size > 0):
            return render_template("gameSearchResults.html", listy = ListOfGames)
        else:
            return render_template('gameSearch.html', message = 'No games By that platform Found')


@gameSearch.route('/by_price', methods= ['POST'])
def filterByPrice():
    if request.method == 'POST':
        price = request.form['pricefilter']
        pricenum = float(price)
        gameList = Games.query.all()
        ListOfGames = []
        for game in gameList:
            if(game.price < pricenum ):
                ListOfGames.append(game)

        size = len(ListOfGames)
        if(size > 0):
            return render_template("gameSearchResults.html", listy = ListOfGames)
        else:
            return render_template('gameSearch.html', message = 'No games under that Price were found')
