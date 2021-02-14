

from flask import Flask, render_template,session,  request, redirect, url_for
from werkzeug import secure_filename
import sqlite3
import os
app = Flask(__name__)
app.secret_key = "asdfghjkl"
# app.debug = True

#initializing the model
# MODEL_PATH = "data/model.pkl"
# model = pickle.load(open('E:/Uday/data/model.pkl','rb'))



#Define home route
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index")
def new():
    return render_template("index.html")


@app.route("/login")
def login():
    if('msg' in request.args):
        messages = request.args['msg'] 
        return render_template("login.html",msg=messages)
    else:
        return render_template("login.html")
    

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html")
    else:
        msg = "Please Login"
        return redirect(url_for('login',msg=msg))

@app.route("/result")
def result():
    if 'username' in session:
        if 'file' in request.args:
            return render_template("result.html",file=file)
        else:
            return render_template("dashboard.html")
    else:
        msg = "Please Login"
        return redirect(url_for('login',msg=msg))

@app.route("/insertUser",methods=['POST'])
def insertUser():
    fullname = request.form['name']
    email = request.form['email']
    username = request.form['uname']
    password = request.form['password']
    mobile = request.form['mobile']
    print(fullname,email,username,password,mobile)
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where username = ? and email  = ?",(username,email))
        records = cur.fetchall()
        if(len(records) > 0):
            msg = "Email already exists"
            return redirect(url_for('login',msg=msg))
        else:
            cur.execute("INSERT INTO users (fullname, email, username, password,mobile) VALUES (?,?,?,?,?)",(fullname,email,username,password,mobile) )
            con.commit()
    msg = "Please Login"
    return redirect(url_for('login',msg=msg))

@app.route("/loginuser",methods=['POST'])
def loginuser():
    email = request.form['email']
    password = request.form['password']
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where password = ? and email  = ?",(password,email))
        records = cur.fetchall()
        if(len(records) > 0):
            print(records)
            session['username'] = request.form['email']
            session['mobile'] = records[0][4]
            return redirect(url_for('dashboard'))
        else:
            msg = "Username or Password is incorrect"
            return redirect(url_for('login',msg=msg))


@app.route('/fileupload', methods = ['GET', 'POST'])
def fileupload():
    os.makedirs(os.path.join('static','uploads'), exist_ok=True)
    f = request.files['file']
    fileName = str(session['mobile'])+'-'+f.filename
    f.save(os.path.join('static/uploads', secure_filename(fileName)))
    print(fileName)
    return render_template("result.html",file=fileName)
	

if __name__ == "__main__":
    app.run()
