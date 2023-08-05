from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

FLASK_DB = "flask_mysql_db"
CATEGORY_TABLE = "categories"

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = FLASK_DB

db = MySQL(app)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/view_categories", methods = ["GET"])
def view_categories():

    cur = db.connection.cursor()
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()
    print(categories)
    cur.close()
    return render_template("categories.html", categories = categories)

@app.route("/add_category", methods = ["POST"])
def add_category():

    name = request.form["name"]
    cur = db.connection.cursor()
    
    try:
        cur.execute(f"INSERT INTO {CATEGORY_TABLE} (name) VALUES (%s)", (name,))
        db.connection.commit()
        cur.close()
    except Exception as e:
        return render_template("add_category_error.html", error_msg = e)
    
    return redirect(url_for("view_categories"))

@app.route("/delete_category/<int:id>")
def delete_category(id):
    cur = db.connection.cursor()

    try:
        cur.execute(f"DELETE FROM {CATEGORY_TABLE} WHERE id = {id}")
        db.connection.commit()
        cur.close()
    except Exception as e:
        return f"There was an error deleting the category --> {e}"
    
    return redirect(url_for("view_categories"))

@app.route("/add_expenses")
def add_expenses():
    cursor = db.connection.cursor()
    print(cursor)
    return render_template("add_expenses.html")

if __name__ == "__main__":
    app.run(debug = True)