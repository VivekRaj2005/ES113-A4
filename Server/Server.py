from  flask import Flask, render_template, send_from_directory
import flask_mysqldb
import os

if not os.path.exists("Server.py"):
    raise RuntimeError("Incorrect Working Directory: set directory to Server")

app = Flask(__name__, template_folder='../Template', static_folder='../Static')


# Icon File 
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("../Static", 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def Home():
    return render_template("Home.html")

if __name__ == "__main__":
    app.run(debug=True)
