from  flask import Flask, render_template, send_from_directory, request
from flask_mysqldb import MySQL
import numpy as np
import os

if not os.path.exists("Server.py"):
    raise RuntimeError("Incorrect Working Directory: set directory to Server")

app = Flask(__name__, template_folder='../Template', static_folder='../Static')
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "kannan"
app.config["MYSQL_DB"] = "es113"
# app.jinja_options["autoescape"] = lambda _: False
mysql = MySQL(app)


# Icon File 
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("../Static", 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def Home():
    return render_template("Home.html")

@app.route('/company', methods=['GET', "POST"])
def Company():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT(name_of_purchaser) FROM eci2;")
        name = cur.fetchall()
        return render_template('CompanyData.html', names=name)
    else:
        company = request.form['Company']
        cur = mysql.connection.cursor()
        cur.execute('select max(purchase) from eci2;')
        maxDate = cur.fetchone()[0]
        cur.execute('select min(purchase) from eci2;')
        mindate = cur.fetchone()[0]
        maxY = int(maxDate.year) + 1
        minY = int(mindate.year)
        data = []
        for x in range(minY, maxY + 1, 1):
            query = f"SELECT count(*), sum(denom) FROM eci2 where name_of_purchaser='{company}' and purchase between '{x}-01-01' and '{x}-12-31';"
            cur.execute(query)
            data.append(tuple([x]) + tuple((cur.fetchone())))
        data1 = np.array(data)
        ctx = list(data1.T[1])
        ctc2 = data1.T[2]
        ctc2[ctc2 == None] = 0
        ctc = list(ctc2.astype(int))
        print(data1.T)
        return render_template('CompanyData Ans.html', years=list(range(minY, maxY + 1, 1)), data=data, ctx=ctx, ctc=ctc, name=company)


        

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


@app.route('/party', methods=['GET', "POST"])
def party():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT(partu) FROM eci1;")
        party = (cur.fetchall())
        return render_template("Party.html", names=party)
    else:
        party = request.form['Party']
        cur = mysql.connection.cursor()
        cur.execute('select max(doe) from eci1;')
        maxDate = cur.fetchone()[0]
        cur.execute('select min(doe) from eci1;')
        mindate = cur.fetchone()[0]
        maxY = int(maxDate.year) + 1
        minY = int(mindate.year)
        data = []
        for x in range(minY, maxY + 1, 1):
            query = f"SELECT count(*), sum(denom) from eci1 join eci2 using(bond) where partu='{party}' and doe between '{x}-01-01' and '{x}-12-31';"
            cur.execute(query)
            data.append(tuple([x]) + tuple((cur.fetchone())))
        print(data)
        data1 = np.array(data)
        ctx = list(data1.T[1])
        ctc2 = data1.T[2]
        ctc2[ctc2 == None] = 0
        ctc = list(ctc2.astype(np.int64))
        print(data1.T)
        return render_template('Party Ans.html', years=list(range(minY, maxY + 1, 1)), data=data, ctx=ctx, ctc=ctc, name=party)

@app.route('/company_party', methods=['GET', 'POST'])
def CompParty():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT(partu) FROM eci1;")
        party = (cur.fetchall())
        return render_template("CoPa.html", names=party)
    else:
        party = request.form['Party']
        query = f"SELECT name_of_purchaser, sum(denom) from eci1 join eci2 using(bond) where partu='{party}' Group by name_of_purchaser"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        data1 = np.array(data)
        ctx = list(data1.T[0].astype(str))
        ctc2 = data1.T[1]
        ctc2[ctc2 == None] = 0
        ctx_ = []
        for x in ctx:
            ctx_.append(str(x))
        ctc = list(ctc2.astype(np.int64))
        return render_template("CoPa Ans.html", company=ctx_, ctx=ctc, data=data, name=party)
    
@app.route('/party_company', methods=['GET', 'POST'])
def PartyComp():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT(name_of_purchaser) FROM eci2;")
        party = (cur.fetchall())
        return render_template("PaCo.html", names=party)
    else:
        party = request.form['Company']
        query = f"SELECT partu, sum(denom) from eci1 join eci2 using(bond) where name_of_purchaser='{party}' Group by partu"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        data1 = np.array(data)
        ctx = list(data1.T[0].astype(str))
        ctc2 = data1.T[1]
        ctc2[ctc2 == None] = 0
        ctx_ = []
        for x in ctx:
            ctx_.append(str(x))
        ctc = list(ctc2.astype(np.int64))
        return render_template("PaCo Ans.html", company=ctx_, ctx=ctc, data=data, name=party)

if __name__ == "__main__":
    app.run(debug=True)
