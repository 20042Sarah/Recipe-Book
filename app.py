from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
DB = "RecipeBook.db"
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#   functions
def add_user(table, add_name, add_password):
    with sqlite3.connect(DB) as connection:
        cursor = connection.cursor()
        # adds username and password to the database
        sql = f"""INSERT INTO {table} (username, password) VALUES (?,?);"""
        cursor.execute(sql, (add_name, add_password))
        connection.commit


def search(username, password):
    # checks if username and password exist in the database
    with sqlite3.connect(DB) as connection:
        cursor = connection.cursor()
        sql = """SELECT * FROM Users WHERE username = ?;"""
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        # check if password was entered correctly
        if user:
            storedpassword = user[2]
            if check_password_hash(str(storedpassword), str(password)):
                print("Correct password.")
                return True, user[0]
            else:
                print(username, storedpassword)
                print("Incorrect password")
                return False, None
        # if user doesn't exist
        else:
            print("User does not exist.")
            return False, None


@app.route("/loginpage")
def loginpage():
    return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    # logs user in
    # gets data from form
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # checks if username and password is in the database
        user_authentication, sqlID = search(username, password)
        search(username, password)
        if user_authentication:
            session['userID'] = sqlID
            print("User authenticated in login function")
            return redirect(url_for("get_userID", userID=sqlID))
        # if username and password don't match database
        else:
            error_message = "Username or password incorrect. Please try again."
            return render_template("login.html", error_message=error_message)
    else:
        # user logged in
        if "userID" in session:
            return redirect(url_for(get_userID, userID=session["userID"]))
        return render_template("login.html")


@app.route("/signup/<error_message>")
def signup(error_message):
    if error_message == 'signup_password_error':
        error_message = "Passwords do not match."
        return render_template("signup.html", error_message=error_message)
    elif error_message == 'signup_user_error':
        error_message = "Username already taken. Please use another name."
        return render_template("signup.html", error_message=error_message)
    else:
        return render_template("signup.html")


@app.route("/add_user")
def add_user_route():
    # page to add user to database
    # get data from form
    username = request.args.get('username')
    password = request.args.get('password')
    confirm_password = request.args.get("confirm")
    with sqlite3.connect(DB) as connection:
        cursor = connection.cursor()
        sql = "SELECT * FROM Users WHERE username = ?;"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        # check if username is already taken
        if user and username == user[1]:
            return redirect("/signup/signup_user_error")
        # check if passwords match
        if password == confirm_password:
            hashed = generate_password_hash(password)
            sql = """INSERT INTO Users (username, password) VALUES (?,?);"""
            cursor.execute(sql, (username, hashed))
            connection.commit
            return redirect(url_for("login"))
        else:
            return redirect("/signup/signup_password_error")


@app.route("/user/<int:userID>")
def get_userID(userID):
    # fetch user ID
    if "userID" in session and session["userID"] == userID:
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            sql = """SELECT * FROM Users WHERE userID = ?;"""
            cursor.execute(sql, (userID,))
            user = cursor.fetchall()
            # get favourites data
            sql = f"""SELECT Recipes.RecipeID, Recipes.Name, Meals.Name, Recipes.Difficulty
            FROM Recipes LEFT JOIN Meals ON Recipes.Meal = Meals. MealID LEFT JOIN Favourites
            ON Recipes.RecipeID = Favourites.recipe WHERE user = '{userID}';"""
            cursor.execute(sql)
            favourites = cursor.fetchall()
        if userID == 1:
            return redirect(url_for("admin"))
        else:
            return render_template("userpage.html", user=user, favourites = favourites)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # logs user out
    session.pop("userID", None)
    # returns to log in page
    return redirect(url_for("login"))


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
    # check if user is signed in
    if 'userID' in session:
        userID = session['userID']
        return render_template('home.html', results=results, meals=meals, food=food, userID=userID)
    else:
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
    except IndexError:
        #   if the recipe name is not in the database an error message is given
        error = 'Page not found. Please check the recipe name.'
        return render_template('error.html', error=error)
    # check if user is signed in
    if 'userID' in session:
        userID = session['userID']
        # check if recipe is a favourite
        sql = f"""SELECT * FROM Favourites WHERE user = {userID} AND recipe = {recipe};"""
        cursor.execute(sql)
        favourites = cursor.fetchall()
        db.close()
        if len(favourites) > 0:
            fav = True
            return render_template('recipe.html', recipe=name, ingred=r1, instr=r2, userID=userID, fav=fav)
        else:
           return render_template('recipe.html', recipe=name, ingred=r1, instr=r2, userID=userID,)
    else:
        db.close()
        return render_template('recipe.html', recipe=name, ingred=r1, instr=r2)


# adding a recipe to favourites
@app.route('/like/<recipe>')
def like(recipe):
    userID = session['userID']
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    sql = """SELECT RecipeID FROM Recipes WHERE Name = '%s';""" % recipe
    cursor.execute(sql)
    recipeID = cursor.fetchall()[0][0]
    sql = f"""INSERT INTO Favourites (user, recipe) VALUES ('{userID}', '{recipeID}');"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect(f'/recipe/{recipe}')


# removing a recipe from favourites
@app.route('/unlike/<recipe>')
def unlike(recipe):
    userID = session['userID']
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    sql = """SELECT RecipeID FROM Recipes WHERE Name = '%s';""" % recipe
    cursor.execute(sql)
    recipeID = cursor.fetchall()[0][0]
    sql = f"""DELETE FROM Favourites WHERE user = '{userID}' AND recipe = '{recipeID}';"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect(f'/recipe/{recipe}')


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


# checks if file is an allowed type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# adds recipe to Recipes table
@app.post('/create_recipe')
def add_recipe():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    name = request.form['Rname']
    meal = request.form['Rmeal']
    diff = request.form['Rdiff']
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filetype = file.filename.rsplit('.', 1)[1].lower()
        filename = f'{name}.{filetype}'
        file.save(os.path.join(UPLOAD_FOLDER, filename))
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
    sql = f"""INSERT INTO Instructions (Recipe, Step, Instruction)
    VALUES ('{recipe}', '{step}', '{instruction}');"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/admin')


#   deleting data
#   deleting recipe
@app.post('/delete_recipe')
def delete_recipe():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    recipe = request.form['recipe']
    table = ['Recipes', 'Favourites', 'Ingredients', 'Instructions']
    column = ['RecipeID', 'recipe', 'Recipe', 'Recipe']
    for i in range(len(table)):
        sql = f"""DELETE FROM {table[i]} WHERE {column[i]} = '{recipe}';"""
        cursor.execute(sql)
        db.commit()
    db.close()
    return redirect('/admin')

#   deleting ingredient
@app.post('/delete_ingred')
def delete_ingred():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    ingredient = request.form['ingredient']
    table = ['Food', 'Ingredients']
    column = ['FoodID', 'Food']
    for i in range(len(table)):
        sql = f"""DELETE FROM {table[i]} WHERE {column[i]} = '{ingredient}';"""
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
    app.secret_key = 'super secret key'
    app.run(debug=True)
