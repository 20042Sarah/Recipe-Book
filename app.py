from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
DB = "RecipeBook.db"

@app.route('/')
def home():
    return 'Welcome'

if __name__ == "__main__":
    app.run(debug=True)
