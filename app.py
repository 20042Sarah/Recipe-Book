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
    #   shows all recipes
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
    sql = """SELECT Recipes.Name FROM Recipes WHERE RecipeID = %s;""" % recipe
    cursor.execute(sql)
    results = cursor.fetchall()
    title = results[0][0]
    sql = """SELECT Food.Name, Ingredients.Quantity FROM Ingredients
        LEFT JOIN Food ON Ingredients.Food = Food.FoodID
        WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    ingredients = cursor.fetchall()
    sql = """SELECT Instructions.Step, Instructions.Instruction FROM
        Instructions WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    instructions = cursor.fetchall()
    db.close()
    print(title)
    print("")
    headings = ["Food", "Quantity"]
    display(ingredients, headings)
    print("")
    headings = ["Step", "Instruction"]
    display(instructions, headings)


def show_meal(meal):
    #   shows recipes for a meal
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT Recipes.Name, Meals.Name FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID WHERE Meal = %s;""" % meal
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    headings = ["Recipe", "Meal"]
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


#   show_all_recipes()
#   show_recipe(1)
show_meal(5)
#   show_ingredient(2)
