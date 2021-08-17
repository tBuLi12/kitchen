from flask import Flask, json, request
import MySQLdb
import datetime


app = Flask(__name__)


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
        date = datetime.date.today().strftime('%Y-%m-%d')
        cursor.execute(f"UPDATE recipes SET last='{date}' WHERE name='{name}'")
        dbConnection.commit()


def addRecipe(name):
    with dbConnection as cursor:
        cursor.execute(f"INSERT INTO recipes (name) VALUES ('{name}')")
        dbConnection.commit()


@app.route('/', methods=['GET'])
def home():
    with open('index.html') as page:
        return page.read()


@app.route('/recipes', methods=['GET', 'POST'])
def getRecipes():
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