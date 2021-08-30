from flask import Flask,render_template,redirect, request,session

import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

@app.route('/')
def info():
     return render_template('info.html')

@app.route('/regist')
def regist():
    if "user_id" in session:
        return redirect('/top')
    else:
        return render_template('regist.html')

@app.route('/regist', methods=["post"])
def regist_post():
    name = request.form.get("member_name")
    password = request.form.get("member_pass")
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO member VALUES (null, ?, ?)",(name,password))
    connect.commit()
    connect.close()
    return redirect('/login')

@app.route('/login')
def login():
    if "user_id" in session:
        return redirect('/top')
    else:
        return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_post():
    name = request.form.get("member_name")
    password = request.form.get("member_pass")
    print(name, password)
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    query = "SELECT id FROM member WHERE name = ? AND pass = ?"
    cursor.execute(query,(name, password))
    id = cursor.fetchone()
    connect.close()
    if id is None:
        return redirect('/login')
    else:
        session["user_id"] = id
        return redirect('/top')

@app.route('/top')
def top():
     return render_template('top.html')

@app.route('/mypage')
def mypage():
    return render_template('my.html')

@app.route('/sakusei')
def sakusei():
    return render_template('sakusei.html')

@app.route('/lanking')
def lanking():
    return render_template('lanking.html')

@app.errorhandler(404)
def notfound(code):
    return "404だよ🐈"

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)


