from  flask import Flask, render_template, send_from_directory, request
from flask_mysqldb import MySQL
import os

if not os.path.exists("Server.py"):
    raise RuntimeError("Incorrect Working Directory: set directory to Server")

app = Flask(__name__, template_folder='../Template', static_folder='../Static')
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "kannan"
app.config["MYSQL_DB"] = "es113"
mysql = MySQL(app)


# Icon File 
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("../Static", 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def Home():
    return render_template("Home.html")

@app.route("/filter", methods=['GET', "POST"])
def Filter():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT(partu) FROM eci1;")
        party = (cur.fetchall())
        party = (("ALL", ), ) + party
        cur.execute("SELECT DISTINCT(name_of_purchaser) FROM eci2;")
        name = cur.fetchall()
        name = (("ALL",),) + name
        return render_template("Filter.html", parties=party, names=name)
    if request.method == "POST":
        # print(dict(request.form))
        doe=request.form['date']
        bond=request.form['bondno']
        pp = request.form['party']
        co=request.form['Company']
        print(doe, bond, pp, co)
        if (doe == "" and bond == "" and pp == "ALL" and co=="ALL"):
            return render_template("Filter Ans.html", error=True, data=[])
        else:
            query = "select referenceno, partu, name_of_purchaser, bond, status_  from eci1 join eci2 using(bond) where "
            if doe != "":
                query += f"doe='{doe}'"
            if bond != "":
                if doe != "":
                    query += " and "
                query += f"bond={bond}"
            if pp != "ALL":
                if doe != "" or bond != "":
                    query += " and "
                query += f"partu='{pp}'"
            if co != "ALL":
                if doe != "" or bond != "" or pp != "ALL":
                    query += " and "
                query += f"name_of_purchaser='{co}'"
            query += ";"
            print(query)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return render_template("Filter Ans.html", error=False, data=list(data))

if __name__ == "__main__":
    app.run(debug=True)
