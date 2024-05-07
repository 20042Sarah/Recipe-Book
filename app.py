#   main application for database
import sqlite3

#   constants
DBNAME = "RecipeBook.db"
INTWIDTH = 5
STRWIDTH = 10

#   functions


def show_all_recipes():
    #   shows instructions and ingredients for a recipe
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


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


def show_ingredient(food):
    #   show recipes that contain an ingredient
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Ingredients WHERE Food = %s;""" % food
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


#   menu
print(show_all_recipes())
print(show_recipe(1))
print(show_meal(5))
print(show_ingredient(2))
