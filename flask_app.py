from flask import (
    Flask,
    json,
    request,
    redirect,
    url_for,
    session,
    render_template
)
import MySQLdb
import datetime


app = Flask(__name__)
app.secret_key = '1k09&ebq17&bd(o]=aQ!$bb'


class DbConnection:
    def __init__(self, host, user, password, dbName):
        self.host = host
        self.user = user
        self.password = password
        self.dbName = dbName
        self.connection = None

    def __enter__(self):
        self.connection = MySQLdb.connect(
            self.host,
            self.user,
            self.password,
            self.dbName
        )
        return self.connection.cursor()

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def commit(self):
        self.connection.commit()


dbConnection = DbConnection(
            "tbuli12.mysql.pythonanywhere-services.com",
            "tbuli12",
            "livjmos35",
            "tbuli12$kitchen"
        )


def pullRecipes():
    with dbConnection as cursor:
        cursor.execute("SELECT name, last FROM recipes ORDER BY last")
        recipeNames = cursor.fetchall()
    return [{"name": name, "date": last} for name, last in recipeNames]


def recipeSetdate(name):
    with dbConnection as cursor:
        args = (datetime.date.today().strftime('%Y-%m-%d'), name)
        cursor.execute("UPDATE recipes SET last=%s WHERE name=%s", args)
        dbConnection.commit()


def addRecipe(name):
    with dbConnection as cursor:
        cursor.execute("INSERT INTO recipes (name) VALUES (%s)", (name,))
        dbConnection.commit()


@app.route('/', methods=['GET'])
def homeRoute():
    if 'username' in session:
        return render_template('index.html', loggedin=True)
    else:
        return redirect(url_for('loginRoute'))


@app.route('/login', methods=['GET', 'POST'])
def loginRoute():
    if request.method == 'GET':
        return render_template('login.html', loggedin=('username' in session))
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('homeRoute'))


@app.route('/logout', methods=['GET'])
def logoutRoute():
    session.pop('username', None)
    return redirect(url_for('loginRoute'))


@app.route('/recipes', methods=['GET', 'POST'])
def recipesRoute():
    if request.method == 'GET':
        return json.dumps(pullRecipes())
    if request.method == 'POST':
        try:
            if request.form["op"] == "new":
                addRecipe(request.form["name"])
                return "added"
            else:
                recipeSetdate(request.form["name"])
        except Exception as e:
            return str(e)
        return "date set"


if __name__ == '__main__':
    app.run()
