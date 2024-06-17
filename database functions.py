#   main application for database
import sqlite3

#   constants
DBNAME = "RecipeBook.db"
COLWIDTH = 10

#   functions


def display(results, headings):
    for column in range(len(headings)):
        heading = headings[column][0]
        print(heading, (COLWIDTH - len(heading)) * " ", end=" | ")
    print()
    for row in results:
        for column in range(len(row)):
            cell = row[column]
            print(cell, (COLWIDTH - len(str(cell))) * " ",  end=" | ")
        print()
    print("")


def show_all_recipes():
    #   shows all recipes
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT Recipes.RecipeID AS ID, Recipes.Name AS Recipe,
        Meals.Name AS Meal FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID;"""
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = cursor.description
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
    sql = """SELECT Food.Name AS Ingredient, Ingredients.Quantity
        FROM Ingredients LEFT JOIN Food ON Ingredients.Food = Food.FoodID
        WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    ingredients = cursor.fetchall()
    ingredheadings = cursor.description
    sql = """SELECT Instructions.Step, Instructions.Instruction FROM
        Instructions WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    instructions = cursor.fetchall()
    instrucheadings = cursor.description
    db.close()
    print(title)
    print("")
    display(ingredients, ingredheadings)
    display(instructions, instrucheadings)


def show_meal(meal):
    #   shows recipes for a meal
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT Meals.Name FROM Meals WHERE MealID = %s;""" % meal
    cursor.execute(sql)
    results = cursor.fetchall()
    title = results[0][0]
    sql = """SELECT Recipes.Name AS Recipe FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID WHERE Meal = %s;""" % meal
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = cursor.description
    db.close()
    print(title)
    print("")
    display(results, headings)


def show_ingredient(food):
    #   show recipes that contain an ingredient
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT Food.Name FROM Food WHERE FoodID = %s;""" % food
    cursor.execute(sql)
    results = cursor.fetchall()
    title = results[0][0]
    sql = """SELECT Recipes.Name AS Recipe, Ingredients.Quantity
        FROM Ingredients LEFT JOIN Recipes
        ON Ingredients.Recipe = Recipes.RecipeID WHERE Food = %s;""" % food
    cursor.execute(sql)
    results = cursor.fetchall()
    headings = cursor.description
    db.close()
    print(title)
    print("")
    display(results, headings)


def displayrecipe(name):
    db = sqlite3.connect(DBNAME)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE Recipes.Name = '%s';""" % name
    cursor.execute(sql)
    results = cursor.fetchall()
    recipe = results[0][0]
    sql = """SELECT Food.Name AS Ingredient, Ingredients.Quantity,
        Ingredients.Measure FROM Ingredients LEFT JOIN Food
        ON Ingredients.Food = Food.FoodID WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    results = cursor.fetchall()
    r1 = []
    for i in results:
        if i[2] is None:
            r1.append((i[0], i[1], ""))
        else:
            r1.append(i)
    sql = """SELECT Instructions.Step, Instructions.Instruction FROM
        Instructions WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    #   r2 = cursor.fetchall()
    db.close()
    return r1


print(displayrecipe(input()))
