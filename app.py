from sqlite3.dbapi2 import connect
from typing import ContextManager
from flask import Flask,render_template,redirect, request,session
import datetime
import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

now_time = datetime.datetime.now()
print(now_time)



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
    connect = sqlite3.connect("seisaku.db")
    c = connect.cursor()
    c.execute("SELECT name FROM lanking")
    lanking_py = []
    # a = c.fetchall()
    # print("aaaaaaa")
    # print(a)
    for row in c.fetchall():
        lanking_py.append({"name":row[0]})
    print(row)
    connect.close()

    return render_template('top.html',items = lanking_py)
    


@app.route('/mypage')
def mypage():
    if "user_id" in session:
        user_id = session["user_id"][0]
        connect = sqlite3.connect('seisaku.db')
        cursor = connect.cursor()
        cursor.execute("SELECT name FROM user WHERE id = ?",(user_id,))
        user_name = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM lanking WHERE user_id = ?",(user_id,))
        a_py = []
        for row in cursor.fetchall():
            a_py.append({"name":row[0]})
        connect.close()
        return render_template('my.html',name = user_name, aaaa = a_py)
    else:
        return redirect('/login')





#チャット作成中

@app.errorhandler(404)
def notfound(code):
    return "404だよ🐈"

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect('/')

@app.route("/lanking_name")
def lanking_name():
    return render_template("lanking_name.html")

@app.route("/lanking_name",methods=['POST'])
def lanking_name_post():
    if "user_id" in session:
        name = request.form.get("lanking_name")
        now = datetime.datetime.now()
        user_id = session['user_id'][0]
        print(user_id)
        conn = sqlite3.connect('seisaku.db')
        c = conn.cursor()
        c.execute("INSERT INTO lanking VALUES (null,?,?,?)",(name,now,user_id))
        conn.commit()
        c.close()
        url = "/sakusei/" + name
        return redirect(url)


@app.route("/sakusei/<name>")
def sakusei(name):
    
    conn = sqlite3.connect('seisaku.db')
    c = conn.cursor()
    c.execute("SELECT id from lanking WHERE name = ?",(name,))
    conn.commit()
    c.close()
    return render_template("sakusei.html",name = name)

@app.route('/sakusei',methods=['POST'])
def sakusei_post():
    name = request.form.get("name")

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
    
    # c.execute("INSERT INTO lanking VALUES (null,?,now,null)",(id,name,created_at,user_id))
    print(id)
    c.execute("SELECT id FROM lanking WHERE name = ?",(name,))
    lanking_id = c.fetchone()[0]
    lanking_id = int(lanking_id)
    print("うんこうんこうんこ")
    print(kouho_1)
    print(lanking_id)
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_1,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_2,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_3,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_4,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_5,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_6,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_7,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_8,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_9,lanking_id))
    c.execute("INSERT INTO content(id,candidate,vote,lanking_id) VALUES (null,?,0,?)",(kouho_10,lanking_id))

    now = datetime.datetime.now()
    print(now)
    # print(kouho)
    # print(id)
    # print(touhyou)
    conn.commit()
    c.close()
    url = "/lanking/" + name
    return redirect(url)

@app.route("/lanking/<name>")
def lanking(name):
    if "user_id" in session:
        user_id = session["user_id"][0]
        print(user_id)
        connect = sqlite3.connect('seisaku.db')
        cursor = connect.cursor()
        cursor.execute("SELECT id FROM lanking WHERE name = ?",(name,))
        lanking_id = cursor.fetchone()[0]
        cursor.execute("SELECT (SELECT name FROM user WHERE id = ?), comment, user_id, lanking_id, time FROM bbs WHERE lanking_id = ?",(user_id,lanking_id))
        bbs_info = cursor.fetchall()
        print(bbs_info)
        bbs_list = []
        for row in bbs_info:
            bbs_list.append({"name":row[0],"comment":row[1],"user_id":row[2],"lanking_id":row[3],"time":row[4]})
        cursor.execute("SELECT * FROM content WHERE lanking_id = (SELECT id FROM lanking WHERE name = ?) ORDER BY vote DESC",(name,))
        lanking_py = []
        for row in cursor.fetchall():
            lanking_py.append({"id":row[0],"candidate":row[1],"vote":row[2],"lanking_id":row[3]})
        connect.close()
        return render_template('lanking.html' ,items = lanking_py,name = name, html_bbs = bbs_list)

@app.route("/lanking_post/<int:id>",methods=["POST"])
def lanking_post(id):
    user_id = session["user_id"][0]
    name = request.form.get("name")
    print("aaaa")
    print(id)
    print(name)
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    cursor.execute("SELECT vote_flag FROM user_vote WHERE candidate_id = ? AND user_id = ? ",(id,user_id))
    flag = cursor.fetchone()
    print("aaaaaaaa")
    print(flag)
    if flag == None:
        cursor.execute("INSERT INTO user_vote VALUES (null,?,?,0)",(user_id,id))
        cursor.execute("UPDATE content SET vote = vote + 1 WHERE id = ?",(id,))
        connect.commit()
    connect.commit()

    connect.close()
    url = "/lanking/" + name
    return redirect(url)


@app.route("/lanking_a")
def lanking_a(name):
    user_id = session["user_id"][0]
    connect = sqlite3.connect("seisaku.db")
    c = connect.cursor()
    c.execute("SELECT * FROM lanking WHERE lanking_id = (SELECT id FROM lanking WHERE name = ?)",(name,))
    lanking_py = []
    for row in c.fetchall():
        lanking_py.append({"id":row[0],"name":row[1],"creaited_at":row[2],"user_id":row[3]})
        connect.close()
        url = "/lanking/" + name
    return redirect(url,items = lanking_py,name = name,)

@app.route('/add/<name>', methods=["POST"])
def add_post(name):
    time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    user_id = session["user_id"][0]
    comment = request.form.get('coment')
    connect = sqlite3.connect('seisaku.db')
    
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM lanking WHERE name = ?",(name,))
    lanking_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO bbs values (null,?,?,?,?)",(comment,user_id,lanking_id,time))
    connect.commit()
    cursor.close()
    url = "/lanking/" + name

    return redirect(url)



if __name__ == "__main__":
    app.run(debug=True)