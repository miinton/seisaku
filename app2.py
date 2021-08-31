from flask import Flask,render_template,redirect, request,session

import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

@app.route('/')
def info():
     return render_template('info.html')

@app.route('/regist')
def regist():
    if "id" in session:
        return redirect('/top')
    else:
        return render_template('regist.html')

@app.route('/regist', methods=["post"])
def regist_post():
    name = request.form.get("name")
    password = request.form.get("user_pass")
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO user VALUES (null, ?, ?)",(name,password))
    connect.commit()
    connect.close()
    return redirect('/login')

@app.route('/login')
def login():
    if "id" in session:
        return redirect('/top')
    else:
        return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_post():
    name = request.form.get("name")
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
        session["id"] = id
        return redirect('/top')




@app.route('/top')
def top():


     return render_template('top.html')

@app.route('/mypage')
def mypage():
    if "id" in session:
        id = session["id"][0]
        connect = sqlite3.connect('seisaku.db')
        cursor = connect.cursor()
        cursor.execute("SELECT name FROM user WHERE id = ?",(id,))
        name = cursor.fetchone()[0]
        connect.close()
        return render_template('my.html',name = name)
    else:
        return redirect('/login')




@app.route('/logout')
def logout():
    session.pop("id",None)
    return render_template('login.html') 

@app.route('/top')
def top_top():
     return render_template('top.html')

@app.route("/sakusei")
def sakusei():
    return render_template("sakusei.html")


@app.route('/sakusei',methods=['POST'])
def sakusei_post():
    lanking_name = request.form.get("lanking_name")
    kouho_1 = request.form.get("kouho_1")
    kouho_2 = request.form.get("kouho_2")
    kouho_3 = request.form.get("kouho_3")
    kouho_4 = request.form.get("kouho_4")
    kouho_5 = request.form.get("kouho_5")
    kouho_6 = request.form.get("kouho_6")
    kouho_7 = request.form.get("kouho_7")
    kouho_8 = request.form.get("kouho_8")
    kouho_9 = request.form.get("kouho_9")
    kouho_10 = request.form.get("kouho_10")


    conn = sqlite3.connect('seisaku.db')
    c = conn.cursor()
    c.execute("INSERT INTO sakusei values(?,?,?,?,?,?,?,?,?,?,?)",(lanking_name,kouho_1,kouho_2,kouho_3,kouho_4,kouho_5,kouho_6,kouho_7,kouho_8,kouho_9,kouho_10))
    conn.commit()
    c.close()
    return render_template("/lanking")

@app.route("/lanking")
def lanking():
    return render_template("lanking.html")


# @app.route('/lanking')
# def lanking():
#     if "id" in session:
#         conn = sqlite3.connect('list_test.db')
#         c = conn.cursor()
#         c.execute("SELECT * from list_test")
#         task_list_py = []
#         for row in c.fetchall():
#             task_list_py.append({"tpl_id":row[0],"tpl_task":row[1],"task_id":row[2]})
#         c.close()
#         return render_template('task.html',tpl_task_list=task_list_py)

if __name__ == "__main__":
    app.run(debug=True)