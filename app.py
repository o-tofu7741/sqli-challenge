import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        if username and password:
            create_db()
            db_name = "TEST.db"
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()
            print(
                f"select * from users where username = '{username}' and password = '{password}'"
            )
            res = cur.execute(
                f"select * from users where username = '{username}' and password = '{password}'"
            )
            if res.fetchone() is not None:
                res_username, res_password = res.fetchone()
                print(res_username, res_password,res.fetchone())
                conn.close()
                return render_template(
                    "profile.html", username=res_username, password=res_password
                )
        return render_template("login.html", result="ログイン失敗")

    return render_template("login.html", result=None)


# @app.route("/OSCi", method=["GET", "POST"])
# def osci():
#     if request.method == "POST":
#         expression = request.form.get("expression", "")
#         try:
#             result = eval(expression)
#         except Exception as e:
#             result = str(e)
#         return render_template("index.html", expression=expression, result=result)
#     return render_template("index.html", expression="", result="")


def create_db():
    db_name = "TEST.db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    try:
        cur.execute("create table users(username,password)")
    except Exception as e:
        print(e)
    cur.execute("insert into users values(?,?)", ("admin", "hogehoge"))
    cur.execute("insert into users values(?,?)", ("bob", r"flag{i_am_Bob_Marley}"))
    cur.execute("insert into users values(?,?)", ("alice", "alice"))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
    app.run()
