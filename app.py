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
    name = request.form.get("user_name")
    password = request.form.get("user_pass")
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO user VALUES (null, ?, ?)",(name,password))
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
    name = request.form.get("user_name")
    password = request.form.get("user_pass")
    print(name, password)
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    query = "SELECT id FROM user WHERE name = ? AND password = ?"
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
    if "user_id" in session:
        user_id = session["user_id"][0]
        connect = sqlite3.connect('seisaku.db')
        cursor = connect.cursor()
        cursor.execute("SELECT name FROM user WHERE id = ?",(user_id,))
        user_name = cursor.fetchone()[0]
        connect.close()
        return render_template('my.html',name = user_name)
    else:
        return redirect('/login')

@app.route("/sakusei")
def sakusei():
    return render_template("sakusei.html")

@app.route('/sakusei',methods=['POST'])
def sakusei_post():
    task = request.form.get("task")


    conn = sqlite3.connect('seisaku.db')
    c = conn.cursor()
    c.execute("INSERT INTO sakusei values(?,?,?,?,?,?,?,?,?,?,?)",(lanking_name,kouho_1,kouho_2,kouho_3,kouho_4,kouho_5,kouho_6,kouho_7,kouho_8,kouho_9,kouho_10,))
    conn.commit()
    c.close()
    return render_template("/lanking")

@app.route("/lanking")
def lanking():
    return render_template("lanking.html")

#チャット作成中

@app.errorhandler(404)
def notfound(code):
    return "404だよ🐈"

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)