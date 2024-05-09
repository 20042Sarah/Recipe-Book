from flask import Flask, render_template
app = Flask(__name__)
DB = "RecipeBook.db"


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def test():
    return render_template('test.html')


if __name__ == "__main__":
    app.run(debug=True)
