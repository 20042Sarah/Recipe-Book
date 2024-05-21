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
        ON Recipes.Meal = Meals.MealID;"""
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return render_template('home.html', results=results)


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
        sql = """SELECT Food.Name AS Ingredient, Ingredients.Quantity
            FROM Ingredients LEFT JOIN Food ON Ingredients.Food = Food.FoodID
            WHERE Recipe = %s;""" % recipe
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
