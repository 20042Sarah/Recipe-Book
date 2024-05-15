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
    return render_template('home.html', results = results)

#   @app.route('/recipe/<recipe>')
    #   def recipe(name):


if __name__ == "__main__":
    app.run(debug=True)
