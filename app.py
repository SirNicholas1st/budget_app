from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime

FLASK_DB = "flask_mysql_db"
CATEGORY_TABLE = "categories"
EXPENSE_TABLE = "expenses"

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
    cur.close()
    
    return render_template("categories.html", categories = categories)

@app.route("/add_category", methods = ["POST"])
def add_category():
    cur = db.connection.cursor()

    name = request.form["name"]
    
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

@app.route("/view_expenses", methods = ["GET", "POST"])
def add_expense():
    
    if request.method == "POST":
        cur = db.connection.cursor()

        expense_date = request.form["expense_date"]
        expense_category_str = request.form["category"]
        expense_amount = request.form["expense_amount"].replace(",", ".")
        
        '''
        To avoid duplicate information accross the tables we will use
        the category id from the categories table, this will allow the use of joins.
        '''
        fetch_category_id_sql = f"""SELECT id
                                    FROM {CATEGORY_TABLE}
                                    WHERE name = '{expense_category_str}'
                                    LIMIT 1;
                                    """
        cur.execute(fetch_category_id_sql)
        expense_category_id = cur.fetchone()[0]
        
        try:
            insert_expense_query = f""" INSERT INTO {EXPENSE_TABLE}
                                (expenseDate, amount, category)
                                VALUES ('{expense_date}', {expense_amount}, {expense_category_id});
                                """
            cur.execute(insert_expense_query)
            db.connection.commit()
            
        except ValueError as e:
            render_template("add_expense_error.html", error_msg = e)

    # categories for drop down menu.
    cur = db.connection.cursor()
    cur.execute(f"SELECT name FROM {CATEGORY_TABLE}")
    categories = cur.fetchall()
    
    # Expenses for the html.
    expense_query = f"""SELECT a.id, expenseDate, b.name, amount
                        FROM {EXPENSE_TABLE} a
                        LEFT JOIN {CATEGORY_TABLE} b
                        ON a.category = b.id
                        ORDER BY expenseDate;
                        """
    cur.execute(expense_query)
    expenses = cur.fetchall()
    cur.close()

    return render_template("expenses.html", categories = categories, expenses = expenses)

@app.route("/delete_expense/<int:id>")
def delete_expense(id):
    cur = db.connection.cursor()

    cur.execute(f"DELETE FROM {EXPENSE_TABLE} WHERE id = {id}")
    db.connection.commit()
    cur.close()

    return redirect(url_for("add_expense"))


if __name__ == "__main__":
    app.run(debug = True)