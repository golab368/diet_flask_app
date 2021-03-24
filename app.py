from flask import Flask, request, render_template, redirect, url_for
from spoon_connector import *
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.secret_key = os.environ['SECRET_KEY']


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        query_day_or_week = request.form['selection']
        if query_day_or_week == 'day':
            return redirect('/day')
        else:
            return redirect('/week/')
    return render_template("homepage.html")


@app.route('/day')
def meals_for_day():
    meal_plan_for_day = get_meal_plan_for_day()

    return render_template("day.html", meal_plan_for_day=meal_plan_for_day)


@app.route('/week/')
def meals_for_week():
    get_meals_list = get_meal_plan_for_week()

    page_number = request.args.get('day', "monday")

    days_in_week = [
        {"day": "monday", "active": ""},
        {"day": "tuesday", "active": ""},
        {"day": "wednesday", "active": ""},
        {"day": "thursday", "active": ""},
        {"day": "friday", "active": ""},
        {"day": "saturday", "active": ""},
        {"day": "sunday", "active": ""},
    ]

    for button in days_in_week:
        if button['day'] == page_number:
            button['active'] = 'active'

    meals_list = get_meals_list[page_number]

    return render_template("week.html", days_in_week=days_in_week, meals_list=meals_list)


@app.route('/random')
def random():
    random_recipe = get_random_recipe()
    return render_template("random.html", random_recipe=random_recipe)


@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":
        query = request.form['query']
        diet = request.form['diet']
        minCarbs = request.form['minCarbs']
        maxCarbs = request.form['maxCarbs']
        minProtein = request.form['minProtein']
        maxProtein = request.form['maxProtein']
        minCalories = request.form['minCalories']
        maxCalories = request.form['maxCalories']
        minFat = request.form['minFat']
        maxFat = request.form['maxFat']
        maxReadyTime = request.form['maxReadyTime']

        result1 = serch_by_values(query, diet=None,
                                 minCarbs=None, maxCarbs=None,
                                 minProtein=None, maxProtein=None,
                                 minCalories=None, maxCalories=None,
                                 minFat=None, maxFat=None,
                                 maxReadyTime=None, how_many_recepies=3)

        result2 = [get_by_id(i['id']) for i in result1["results"]]

        return render_template("results.html", result1=result1, result2=result2)

    else:
        return render_template("search.html")

@app.route("/about")
def about():

    return render_template("about.html")


@app.context_processor
def utility_processor():
    def spoon_image_url(path):
        return get_dish_image(path)
    return {"spoon_image_url": spoon_image_url}

if __name__ == '__main__':
    app.run(debug=True)
