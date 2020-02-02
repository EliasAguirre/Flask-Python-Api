from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import sqlite3
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# //Flask has a default GET http method as you start the simple server
# as the server is running locally, in the command line you can run curl http://localhost:5000 and it will retrieve the value from this api
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# initial trials - ignore
# class Hobbies(Resource):
#     def get(self):
#         return {
#             'EliasAg': {
#                 'hobby': ['golf',
#                 'piano']
#         },
#         'PersonB': {
#             'hobby': ['hiking']
#             }
#         }

# api.add_resource(Hobbies, '/hobbies')

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Elias'}
    return render_template('index.html', title='Home', user=user)

@app.route("/add")  
def add():  
    return render_template("add.html")  

@app.route("/delete")  
def delete():  
    return render_template("delete.html")  

@app.route("/view")  
def view():  
    con = sqlite3.connect("myDB2.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from myTable")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)   

@app.route('/api/v1/people', methods=['GET'])
def api_name():
    conn = sqlite3.connect('myDB2.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_people = cur.execute('SELECT * FROM myTable;').fetchall()

    return jsonify(all_people)

@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"
    if request.method == "POST":  
        try:  
            name = request.form["name"]  
            age = request.form["age"]   
            with sqlite3.connect("myDB2.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into myTable (name, age) values (?,?)",(name,age))  
                con.commit()  
                msg = "User successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the employee to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  

@app.route("/deleteuser",methods = ["POST"])  
def deleteuser():  
    id = request.form["id"]  
    with sqlite3.connect("myDB2.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from myTable where id = ?",id)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_user.html",msg = msg)   

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404



if __name__ == '__main__':
    app.run(debug=True)

