import os
import requests

# Main connector

def connector(startpoint, querystring=None):
    api_key = os.environ.get("api_key")
    base_url = f"https://api.spoonacular.com/"
    response = requests.get(f"{base_url}{startpoint}{api_key}{querystring}")
    return response.json()


def get_meal_plan_for_day():
    startpoint = 'mealplanner/generate'
    querystring = "timeFrame=day"
    data = connector(startpoint, querystring)
    return data


def get_meal_plan_for_week():
    startpoint = 'mealplanner/generate'
    querystring = "timeFrame=week"
    data = connector(startpoint, querystring)["week"]
    return data


def get_random_recipe():
    startpoint = "recipes/random"
    data = connector(startpoint)['recipes'][0]
    return data


def serch_by_values(query, diet=None,
                    minCarbs=None, maxCarbs=None,
                    minProtein=None, maxProtein=None,
                    minCalories=None, maxCalories=None,
                    minFat=None, maxFat=None,
                    maxReadyTime=None, how_many_recepies=4):
    startpoint = "recipes/complexSearch"
    querystring = f"query={query}&{diet}&{minCarbs}&{maxCarbs}&{minProtein}&{maxProtein}&{minCalories}&{maxCalories}&{minFat}&{maxFat}&{maxReadyTime}&number={how_many_recepies}"
    data = connector(startpoint, querystring)
    return data


def get_by_id(id):
    startpoint = f"recipes/{id}/information"
    querystring = "includeNutrition=false"
    data = connector(startpoint, querystring)
    return data


def get_by_ingredients(ingredients, how_many=6):
    startpoint = "recipes/findByIngredients"
    querystring = f"ingredients={ingredients}&number={how_many}"
    data = connector(startpoint, querystring)
    return data


def get_dish_image(poster_api_path):
    base_url = "https://webknox.com/recipeImages/"
    endpoint = "-556x370.jpg"
    return f"{base_url}/{poster_api_path}{endpoint}"
