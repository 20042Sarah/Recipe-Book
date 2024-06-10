from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
DB = "RecipeBook.db"


#   home page
@app.route('/')
def allrecipes():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    sql = """SELECT Recipes.RecipeID, Recipes.Name,
        Meals.Name, Recipes.Difficulty FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID ORDER BY Recipes.Name;"""
    cursor.execute(sql)
    results = cursor.fetchall()
    sql = """SELECT Name from Meals;"""
    cursor.execute(sql)
    meals = cursor.fetchall()
    cursor = db.cursor()
    sql = """SELECT Name from Food ORDER BY Food.Name;"""
    cursor.execute(sql)
    f = cursor.fetchall()
    db.close()
    return render_template('home.html', results=results, meals=meals, food=f)


#   filters by meal
@app.route('/meal/<filter>')
def filtermeal(filter):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    try:
        sql = """SELECT * FROM Meals WHERE Meals.Name = '%s';""" % filter
        cursor.execute(sql)
        results = cursor.fetchall()
        meal = results[0][0]
        sql = """SELECT Recipes.RecipeID, Recipes.Name,
        Meals.Name, Recipes.Difficulty FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID WHERE Meal = '%s' ORDER BY Recipes.Name;""" % meal
        cursor.execute(sql)
        results = cursor.fetchall()
        sql = """SELECT Name from Meals;"""
        cursor.execute(sql)
        meals = cursor.fetchall()
        sql = """SELECT Name from Food ORDER BY Food.Name;"""
        cursor.execute(sql)
        f = cursor.fetchall()
        db.close()
    except IndexError:
        #   if the meal is not in the database an error message is given
        error = 'Page not found. Please check the address.'
        return render_template('error.html', error=error)
    return render_template('home.html', results=results, meals=meals, food=f)


#   filters by difficulty
@app.route('/diff/<filter>')
def filterdifficulty(filter):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    try:
        sql = """SELECT Recipes.RecipeID, Recipes.Name,
        Meals.Name, Recipes.Difficulty FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID WHERE Difficulty = '%s';""" % filter
        cursor.execute(sql)
        results = cursor.fetchall()
        sql = """SELECT Name from Meals;"""
        cursor.execute(sql)
        meals = cursor.fetchall()
        cursor = db.cursor()
        sql = """SELECT Name from Food;"""
        cursor.execute(sql)
        f = cursor.fetchall()
        db.close()
    except IndexError:
        error = 'Page not found. Please check the address.'
        return render_template('error.html', error=error)
    return render_template('home.html', results=results, meals=meals, food=f)


#   filters by ingredients
@app.route('/food/<filter>')
def filteringredients(filter):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    try:
        sql = """SELECT * FROM Food WHERE Food.Name = '%s';""" % filter
        cursor.execute(sql)
        results = cursor.fetchall()
        food = results[0][0]
        sql = """SELECT Ingredients.Recipe FROM Ingredients LEFT JOIN Recipes
        ON Ingredients.Recipe = Recipes.RecipeID WHERE Food = '%s';""" % food
        cursor.execute(sql)
        recipes = cursor.fetchall()
        results = []
        for recipe in recipes:
            sql = """SELECT Recipes.RecipeID, Recipes.Name,
            Meals.Name, Recipes.Difficulty FROM Recipes LEFT JOIN Meals
            ON Recipes.Meal = Meals.MealID WHERE RecipeID = '%s';""" % recipe
            cursor.execute(sql)
            result = cursor.fetchall()
            results += result
        sql = """SELECT Name from Meals;"""
        cursor.execute(sql)
        meals = cursor.fetchall()
        cursor = db.cursor()
        sql = """SELECT Name from Food;"""
        cursor.execute(sql)
        f = cursor.fetchall()
        db.close()
    except IndexError:
        error = 'Page not found. Please check the address.'
        return render_template('error.html', error=error)
    return render_template('home.html', results=results, meals=meals, food=f)


#   recipe page
@app.route('/recipe/<name>')
def displayrecipe(name):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    try:
        sql = """SELECT * FROM Recipes WHERE Recipes.Name = '%s';""" % name
        cursor.execute(sql)
        results = cursor.fetchall()
        recipe = results[0][0]
        sql = """SELECT Food.Name AS Ingredient, Ingredients.Quantity,
            Ingredients.Measure FROM Ingredients LEFT JOIN Food
            ON Ingredients.Food = Food.FoodID WHERE Recipe = %s;""" % recipe
        cursor.execute(sql)
        r1 = cursor.fetchall()
        sql = """SELECT Instructions.Step, Instructions.Instruction FROM
            Instructions WHERE Recipe = %s;""" % recipe
        cursor.execute(sql)
        r2 = cursor.fetchall()
    except IndexError:
        #   if the recipe name is not in the database an error message is given
        error = 'Page not found. Please check the recipe name.'
        return render_template('error.html', error=error)
    return render_template('recipe.html', recipe=name, ingred=r1, instr=r2)


#   page not found error page
@app.errorhandler(404)
def page_not_found(error):
    error = 'Page not found. Please check that the address is spelt correctly.'
    return render_template('error.html', error=error)


#   internal server error page
@app.errorhandler(500)
def internal_server_error(error):
    error = 'Internal server error.'
    return render_template('error.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
