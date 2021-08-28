from flask import Flask,render_template,redirect, request,session

import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

@app.route('/')
def info():
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
    # if id is None:
    #     return redirect('/login')
    # else:
    #     session["uer_id"] = id
    return render_template('top.html')



@app.route('/top')
def top(): 
    if "user_id" in session:
        #return render_template('top.html')
        user_id = session["user_id"][0]
        connect = sqlite3.connect('seisaku.db')
        cursor = connect.cursor()
        cursor.execute("SELECT name FROM user WHERE id = ?",(user_id,))
        user_name = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM user WHERE user_id = ?",(user_id,))
        connect.close()
        return render_template('top.html',user_name = user_name)
    else:
        return render_template('login.html') 

# @app.route('/mypage')
# def mypage(): 
#         if "user_id" in session:
#         user_id = session["user_id"][0]
#         connect = sqlite3.connect('seisaku.db')
#         cursor = connect.cursor()
#         cursor.execute("SELECT name FROM user WHERE id = ?",(user_id,))
#         user_name = cursor.fetchone()[0]
#         cursor.execute("SELECT id FROM user WHERE user_id = ?",(user_id,))
#         connect.close()
#         return render_template('mypage.html')

#@app.route('/sakusei')
#def sakusei(): 
#    if "user_id" in session:
#        return redirect('/sakusei') 
#    else:
#        return render_template('login.html') 

# @app.route('/sakusei')
# def sakusei():
#     if "user_id" in session:
#         user_id = session["user_id"][0]
#         connect = sqlite3.connect('seisaku.db')
#         cursor = connect.cursor()
#         #新しいデータベースを作って置き換える
#         cursor.execute("SELECT name FROM member WHERE id = ?",(user_id,))
#         user_name = cursor.fetchone()[0]
#         cursor.execute("SELECT id,task FROM task WHERE user_id = ?",(user_id,))
#         task = cursor.fetchall()
#         # task のままだと使いにづらいので
#         # リストの中にオブジェクトのある形に再代入 [{"id:01", task:やさい}]
#         task_listTYPE = []
#         for row in task:
#             task_listTYPE.append({"id":row[0],"task":row[1]})
#         connect.close()
#         print(task)
#         print(task_listTYPE)
#         return render_template('tasklist.html',html_task = task_listTYPE,user_name = user_name)
#     else:
#         return redirect('/login')

# @app.route('/edit/<int:id>')
# def edit(id):
#     connect = sqlite3.connect('seisaku.db')
#     cursor = connect.cursor()
#     cursor.execute("SELECT task FROM task WHERE id = ?", (id,))
#     task = cursor.fetchone()
#     connect.close()
#     if task is None:
#         return redirect('/seisaku')
#     else:
#         task = taks[0]
#     item = {"id":id,"task":task}
#     return render_template('edit.html',html_item = item)



# @app.route('/edit', methods=["post"])
# def edit_post():
#     task = request.form.get('task')
#     id = request.form.get('id')
#     connect = sqlite3.connect('flasktest.db')
#     cursor = connect.cursor()
#     cursor.execute('UPDATE task SET task = ? WHERE id = ?', (task, id))
#     connect.commit()
#     connect.close()
#     return redirect('/tasklist')

# @app.route('/delete/<int:id>')
# def delete(id):
#     connect = sqlite3.connect('flasktest.db')
#     cursor = connect.cursor()
#     cursor.execute("DELETE FROM task WHERE id = ?",(id,))
#     connect.commit()
#     connect.close()
#     return redirect('/tasklist')


@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return render_template('login.html') 

@app.route('/top')
def top_top():
     return render_template('top.html')



if __name__ == "__main__":
    app.run(debug=True)