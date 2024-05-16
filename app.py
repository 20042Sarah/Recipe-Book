from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
DB = "RecipeBook.db"


@app.route('/')
def allrecipes():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    sql = """SELECT Recipes.RecipeID, Recipes.Name,
        Meals.Name FROM Recipes LEFT JOIN Meals
        ON Recipes.Meal = Meals.MealID;"""
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return render_template('home.html', results=results)


@app.route('/recipe/<name>')
def displayrecipe(name):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    sql = """SELECT * FROM Recipes WHERE Recipes.Name = '%s';""" % name
    cursor.execute(sql)
    results = cursor.fetchall()
    recipe = results[0][0]
    sql = """SELECT Food.Name AS Ingredient, Ingredients.Quantity
        FROM Ingredients LEFT JOIN Food ON Ingredients.Food = Food.FoodID
        WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    ingredients = cursor.fetchall()
    sql = """SELECT Instructions.Step, Instructions.Instruction FROM
        Instructions WHERE Recipe = %s;""" % recipe
    cursor.execute(sql)
    instructions = cursor.fetchall()
    return render_template('recipe.html', recipe=name, ingredients=ingredients, instructions=instructions)


if __name__ == "__main__":
    app.run(debug=True)
