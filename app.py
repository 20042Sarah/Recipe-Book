#   main application for database
import sqlite3

#   constants
DBNAME = "RecipeBook.db"

#   functions


def show_recipe(recipe):
    #   shows instructions and ingredients for a recipe
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE RecipeID = %s;""" % recipe
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def show_meal(meal):
    #   shows recipes for a meal
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE Meal = %s;""" % meal
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


#   show recipes that contain an ingredient

#   menu
