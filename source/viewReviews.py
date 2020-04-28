from flask import Blueprint, render_template, request
from source.models import Reviews

viewReviews = Blueprint("viewReviews", __name__, static_folder='static', static_url_path='../static', template_folder='templates')

@viewReviews.route('', methods= ['POST'])
def searchgames():
    reviewList = Reviews.query.all()
    return render_template('viewReviews.html', reviewList = reviewList)