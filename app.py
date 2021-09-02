import sqlite3

from flask import Flask , render_template , request , redirect , session

app = Flask(__name__)

from datetime import datetime

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

@app.route('/bbs')
def bbs():
    if "user_id"in session:
        user_id = session["user_id"][0]
        lanking_id = 1
        connect = sqlite3.connect('seisaku.db')
        cursor = connect.cursor()
        cursor.execute("SELECT (SELECT name FROM user WHERE id = ?), comment, user_id, lanking_id, time FROM bbs WHERE lanking_id = ?",(user_id,lanking_id))
        bbs_info = cursor.fetchall()
        print(bbs_info)
        bbs_list = []
        for row in bbs_info:
            bbs_list.append({"name":row[0],"comment":row[1],"user_id":row[2],"lanking_id":row[3],"time":row[4]})
        connect.close()
        return render_template('bbs.html', html_bbs = bbs_list)
    else:
        return redirect('/login')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add', methods=["POST"])
def add_post():
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    comment = request.form.get('coment')
    connect = sqlite3.connect('seisaku.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO bbs values (null,?,1,1,?)",(comment,time))
    connect.commit()
    cursor.close()
    return redirect('/bbs')



@app.errorhandler(404)
def notfound(code):
    return "404だよ🐈"

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)