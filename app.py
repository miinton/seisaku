from flask import Flask,render_template,redirect, request,session

import sqlite3

app = Flask(__name__)
app.secret_key = "SUNABACO"

@app.route('/')
def saisyo():
     return render_template('info.html')


# @app.route('/dbtest')
# def dbtest():
#     #データベースに接続
#     connect = sqlite3.connect('seisaku.db')
#     cursor = connect.cursor()
#     #DBに命令
#     cursor.execute("SELECT name,age,address FROM user WHERE id = 1")
#     #SELECTでとってきた内容をuser_infoに代入
#     user_info = cursor.fetchone()
#     #DEの接続を完了
#     connect.close()
#     print(user_info)
#     return render_template('dbtest.html', html_info = user_info)

# @app.route('/add')
# def add_get():
#     if "user_id" in session:
#         return render_template('add.html')
#     else:
#         return redirect('/login')


# @app.route('/add', methods =["post"])
# def add_post():
#     user_id = session["user_id"][0]
#     print(user_id)
#     py_task = request.form.get('task') 
#     connect = sqlite3.connect('seisaku.db')
#     cursor = connect.cursor()
#     cursor.execute("INSERT INTO task VALUES (null,?,?)", (py_task, user_id))
#     #保存ができる
#     connect.commit()
#     connect.close()
#     return redirect('/tasklist')


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
    print(name, password)
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO user VALUES (null, ?, ?)",(name, password))
    connect.commit()
    connect.close()
    return render_template('top.html')

@app.route('/login')
def login():
    if "user_id" in session:
        return render_template('top.html')
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
        session["name"] = name
        return render_template('top.html')

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect('/top')

 @app.route('/mypage')
 def mypage(): 
     return render_template('mypage.html')  

if __name__ == "__main__":
    app.run(debug=True)

#@app.route('/top')
#def top():
    #return render_template('top.html')