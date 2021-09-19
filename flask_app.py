from flask import (
    Flask,
    json,
    request,
    redirect,
    url_for,
    session,
    render_template
)
from threading import Lock
import MySQLdb
import datetime
import bcrypt
from time import time
from string import printable
from random import choice


app = Flask(__name__)
app.secret_key = '1k09&ebq17&bd(o]=aQ!$bb'

suToken = None
suTokenLock = Lock()


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


def authenticate(username, password):
    with dbConnection as cursor:
        cursor.execute("SELECT passhash FROM users WHERE username=%s", (username,))
        result = cursor.fetchall()
        if not result:
            return False
        passHash = cursor.fetchall()[0][0]
    return bcrypt.checkpw(password, passHash)


def signUp(username, password):
    passhash = bcrypt.hashpw(password, bcrypt.gensalt())
    with dbConnection as cursor:
        cursor.execute("INSERT INTO users (username, passhash) VALUES (%s, %s)", (username, passhash))
        dbConnection.commit()


@app.route('/token', methods=['GET'])
def getToken():
    global suToken
    token = ''.join([choice(printable) for i in range(10)])
    with suTokenLock:
        suToken = (time(), token)
    return token


@app.route('/', methods=['GET'])
def homeRoute():
    if 'username' in session:
        return render_template('index.html', loggedin=True)
    else:
        return redirect(url_for('loginRoute'))


@app.route('/signup', methods=['GET', 'POST'])
def signupRoute():
    global suToken
    if request.method == 'GET':
        return render_template('signup.html', loggedin=('username' in session))
    if request.method == 'POST':
        token = request.form['token']
        if suToken and token == suToken[1] and time() - suToken[0] < 60:
            signUp(request.form['username'], request.form['password'])
            return redirect(url_for('loginRoute'))
        else:
            return redirect(url_for('signupRoute'))


@app.route('/login', methods=['GET', 'POST'])
def loginRoute():
    if request.method == 'GET':
        return render_template('login.html', loggedin=('username' in session))
    if request.method == 'POST':
        if authenticate(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('homeRoute'))
        else:
            return redirect(url_for('loginRoute'))


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
