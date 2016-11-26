from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dbconnect import connection
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def main():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])

    return render_template('index.html')

@app.route('/dashboard/', methods = ['POST','GET'])
def loginP():
    #try:
    if request.method == 'POST':
        try:
            c,conn = connection()
            username = request.form['usr']
            pwd = request.form['pwd']


            c.execute("SELECT * FROM user WHERE login = %s AND password = %s", [username, pwd])
            data = c.fetchall()

            if len(data) == 0:
                return render_template('index.html',err='invalid combination of Username and Password')

            id = int(data[0][0])

            session['user'] = id
            return render_template('dashboard.html',user= username)


        except Exception as e:
            return str(e)

    else:
        if 'user' in session:
            return render_template('dashboard.html', user=session['user'])
        else:
            return redirect('/')

@app.route('/shome')
def info():
    if 'user' in session:
        c, conn = connection()
        currentUser = session['user']
        c.execute("select * from application where name  NOT in (select name from userApp where id = %s)",[currentUser])
        data = c.fetchall()

        return render_template('addTemp.html',apps=data)
    else:
        return redirect("/")

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect("/shome")

@app.route('/removeApp/<appName>',methods = ['POST'])
def removeApp(appName):
    try:
        currentUser = session['user']
        c, conn = connection()
        c.execute("delete from userApp where id = %s and name = %s",[currentUser, appName])
        conn.commit()
        return redirect("/dashboard")
    except Exception as e:
        return redirect("/dashboard")

@app.route('/addApp/<appName>',methods = ['POST'])
def addApp(appName):
    try:
        currentUser = session['user']
        c, conn = connection()
        c.execute("insert into userApp values(%s,%s)",[currentUser, appName])
        conn.commit()
        return redirect("/dashboard")
    except Exception as e:
        return redirect("/dashboard")

@app.route('/allapps/')
def showAll():
    if 'user' in session:
        currentUser= session['user']
        c, conn = connection()
        c.execute("select a.name,description,color from userApp as u inner join application as a on u.name=a.name and id=%s",
        [currentUser])
        data = c.fetchall()
        l = []
        for x in data:
            l.append(x)
        return render_template('showApp.html',apps=l)
    else:
        return render_template('showApp.html', warn='Please Log In')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("invalidURL.html")

if __name__ == "__main__":
    app.run(debug=True)