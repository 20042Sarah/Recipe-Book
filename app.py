from flask import Flask, render_template, request, redirect
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
    food = cursor.fetchall()
    db.close()
    return render_template('home.html', results=results, meals=meals, food=food)


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
        ON Recipes.Meal = Meals.MealID WHERE Meal = '%s'
        ORDER BY Recipes.Name;""" % meal
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
        ON Recipes.Meal = Meals.MealID WHERE Difficulty = '%s'
        ORDER BY Recipes.Name;""" % filter
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
        #   gets food id
        sql = """SELECT * FROM Food WHERE Food.Name = '%s'
        ORDER BY Food.Name;""" % filter
        cursor.execute(sql)
        results = cursor.fetchall()
        food = results[0][0]
        #   gets recipe id for recipes that conatin that ingredient
        sql = """SELECT Ingredients.Recipe FROM Ingredients LEFT JOIN Recipes
        ON Ingredients.Recipe = Recipes.RecipeID WHERE Food = '%s';""" % food
        cursor.execute(sql)
        recipes = cursor.fetchall()
        results = []
        for recipe in recipes:
            #   gets recipe data
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
        sql = """SELECT Name from Food ORDER BY Food.Name;"""
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
        #   gets ingredient data
        sql = """SELECT * FROM Recipes WHERE Recipes.Name = '%s';""" % name
        cursor.execute(sql)
        results = cursor.fetchall()
        recipe = results[0][0]
        sql = """SELECT Food.Name AS Ingredient, Ingredients.Quantity,
        Ingredients.Measure FROM Ingredients LEFT JOIN Food
        ON Ingredients.Food = Food.FoodID WHERE Recipe = %s;""" % recipe
        cursor.execute(sql)
        results = cursor.fetchall()
        #   formats the ingredient data better for displaying
        r1 = []
        for i in results:
            try:
                if int(i[1]) == i[1]:
                    if i[2] is None:
                        r1.append((i[0], int(i[1]), ""))
                    else:
                        r1.append((i[0], int(i[1]), i[2]))
                else:
                    if i[2] is None:
                        r1.append((i[0], i[1], ""))
                    else:
                        r1.append(i)
            except ValueError:
                if i[2] is None:
                    r1.append((i[0], i[1], ""))
                else:
                    r1.append(i)
            except TypeError:
                if i[2] is None:
                    r1.append((i[0], i[1], ""))
                else:
                    r1.append(i)
        #   gets instruction data
        sql = """SELECT Instructions.Step, Instructions.Instruction FROM
        Instructions WHERE Recipe = %s;""" % recipe
        cursor.execute(sql)
        r2 = cursor.fetchall()
        db.close()
    except IndexError:
        #   if the recipe name is not in the database an error message is given
        error = 'Page not found. Please check the recipe name.'
        return render_template('error.html', error=error)
    return render_template('recipe.html', recipe=name, ingred=r1, instr=r2)


#   admin page
@app.route('/admin')
def admin():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    sql = """SELECT * from Meals;"""
    cursor.execute(sql)
    meals = cursor.fetchall()
    sql = """SELECT * from Food ORDER BY Food.Name;"""
    cursor.execute(sql)
    food = cursor.fetchall()
    sql = """SELECT * from Recipes ORDER BY Recipes.Name;"""
    cursor.execute(sql)
    recipes = cursor.fetchall()
    db.close()
    return render_template('admin.html', meals=meals, food=food, recipes=recipes)


# adds recipe to Recipes table
@app.post('/create_recipe')
def add_recipe():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    name = request.form['Rname']
    meal = request.form['Rmeal']
    diff = request.form['Rdiff']
    sql = f"""INSERT INTO Recipes (Name, Meal, Difficulty)
    VALUES ('{name}', '{meal}', '{diff}');"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/admin')


# adds data to Ingredients table
@app.post('/add_ingredient')
def add_ingredient():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    recipe = request.form['recipe']
    food = request.form['food']
    quantity = request.form['quan']
    measure = request.form['meas']
    sql = f"""INSERT INTO Ingredients (Recipe, Food, Quantity, Measure)
    VALUES ('{recipe}', '{food}', '{quantity}', '{measure}');"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/admin')


# adds data to Food table
@app.post('/create_ingredient')
def create_ingredient():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    name = request.form['name']
    sql = f"""INSERT INTO Food (Name) VALUES ('{name}');"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/admin')


# adds data to Instructions table
@app.post('/add_step')
def add_step():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    recipe = request.form['recipe']
    step = request.form['step']
    instruction = request.form['instruction']
    sql = f"""INSERT INTO Instructions (Recipe, Step, Instruction) VALUES ('{recipe}', '{step}', '{instruction}');"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/admin')


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
