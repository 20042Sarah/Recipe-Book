#   main application for database
import sqlite3

#   constants
DBNAME = "RecipeBook.db"
COLWIDTH = 10

#   functions


def display(results, headings):
    for column in range(len(headings)):
        heading = headings[column]
        print(heading, (COLWIDTH - len(heading)) * " ", end=" | ")
    print()
    for row in results:
        for column in range(len(row)):
            cell = row[column]
            print(cell, (COLWIDTH - len(str(cell))) * " ",  end=" | ")
        print()


def show_all_recipes():
    #   shows instructions and ingredients for a recipe
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT Recipes.RecipeID, Recipes.Name, Meals.Name FROM Recipes
        LEFT JOIN Meals ON Recipes.Meal = Meals.MealID;"""
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = ["Recipe ID", "Name", "Meal"]
    db.close()
    display(results, headings)


def show_recipe(recipe):
    #   shows instructions and ingredients for a recipe
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE RecipeID = %s;""" % recipe
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = cursor.description
    db.close()
    display(results, headings)


def show_meal(meal):
    #   shows recipes for a meal
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE Meal = %s;""" % meal
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = cursor.description
    db.close()
    display(results, headings)


def show_ingredient(food):
    #   show recipes that contain an ingredient
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Ingredients WHERE Food = %s;""" % food
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = cursor.description
    db.close()
    display(results, headings)


#   menu
print(show_all_recipes())
#   print(show_recipe(1))
#   print(show_meal(5))
#   print(show_ingredient(2))
