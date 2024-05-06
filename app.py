#   main application for database
import sqlite3

#   constants
DBNAME = "RecipeBook.db"

#   functions

#   show instructions and ingredients for a recipe


def show_recipe(recipe):
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE RecipeID = %s;""" % recipe
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

#   show recipes for a meal
#   show recipes that contain an ingredient

#   menu
