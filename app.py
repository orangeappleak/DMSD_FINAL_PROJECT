import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, escape, flash
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(24)


@app.route('/')
def index():
    if 'admin-username' in session:
        return 'Hey, {}!'.format(escape(session['username']))
    return render_template('index.html')


@app.route('/adminLogin', methods=['GET', 'POST'], defaults={'username': ''})
@app.route('/adminLogin/<username>', methods=['GET', 'POST'])
def adminLogin(username):
    if request.method == 'POST':
        conn = get_db_connection()
        admins = conn.execute("SELECT * FROM admins").fetchall()

        username = request.form['admin-username']
        password = request.form['admin-password']

        if (username != ""):
            print("username not null")
            for admin in admins:
                if username == admin['username']:
                    print("found username ", username)
                    if password == admin['password']:
                        print("found password", password)
                        flash("LOGGED IN SUCCESSFULLY")
                        return render_template('admin.html', username=username)

        else:
            flash("INVALID CREDENTIALS PLEASE TRY AGAIN!!!")
            return redirect("/")
        conn.close()
    return render_template('admin.html', username=username)


@app.route('/adminLogin/addReader', methods=['GET', 'POST'])
def addReader():
    conn = get_db_connection()
    readers = conn.execute("SELECT * FROM readers").fetchall()
    conn.close()
    return render_template('addReader.html', readers=readers)


@app.route('/adminLogin/addBranch', methods=['GET', 'POST'])
def addBranch():
    conn = get_db_connection()
    branches = conn.execute("SELECT * FROM branch").fetchall()
    conn.close()
    return render_template('addBranch.html', branches=branches)


@app.route('/adminLogin/addDocument', methods=['GET', 'POST'])
def addDocument():
    conn = get_db_connection()
    documents = conn.execute("SELECT * FROM document").fetchall()
    
    conn.close()
    return render_template('addDocument.html', documents=documents)


@app.route('/adminLogin/addPublisher', methods=['GET', 'POST'])
def addPublisher():
    conn = get_db_connection()
    publishers = conn.execute("SELECT * FROM publisher").fetchall()
    conn.close()
    return render_template('addPublisher.html', publishers=publishers)


@app.route('/addReader', methods=['GET', 'POST'])
def insertReader():
    conn = get_db_connection()
    rname = request.form['reader-name']
    raddress = request.form['reader-address']
    rphone = request.form['reader-phoneno']

    if (rname != "" and raddress != "" and rphone != ""):
        conn.execute(
            "INSERT INTO readers (RNAME, RADDRESS, PHONE_NO) VALUES (?, ?, ?)", (rname, raddress, rphone))
        conn.commit()
    conn.close()
    flash("User added successfully!!!")
    return redirect('/adminLogin/addReader')


@app.route('/addBranch', methods=['GET', 'POST'])
def insertBranch():
    conn = get_db_connection()
    brname = request.form['branch-name']
    braddress = request.form['branch-address']
    if (brname != "" and braddress != ""):
        conn.execute(
            "INSERT INTO branch (LNAME, LOCATION) VALUES (?,?)", (brname, braddress))
        conn.commit()
    conn.close()
    return redirect('/adminLogin/addBranch')

@app.route('/addDocument', methods=['GET', 'POST'])
def insertDocument():
    conn = get_db_connection()
    title = request.form['title']
    pdate = request.form['pdate']
    pid = request.form['pid']
    if (title != "" and pdate!= "" and pid != ""):
        conn.execute(
            "INSERT INTO document (TITLE, PDATE) VALUES (?,?)", (title, pdate))
        conn.commit()
    conn.close()
    return redirect('/adminLogin/addDocument')


@app.route('/readerLogin', methods=['GET', 'POST'])
def readerLogin():
    if request.method == 'POST':
        conn = get_db_connection()
        readers = conn.execute("SELECT * FROM readers").fetchall()
        print(readers)
        readerid = request.form['reader-cardid']
        print("we got reader id = ", readerid)
        for reader in readers:
            print("READER ID = ", reader['RID'])
            if str(readerid) == str(reader['RID']):
                print("found reader")
                readername = reader['RNAME']
                return render_template('reader.html', readerid=readerid, readername=reader['RNAME'], readers=readers)
            else:
                print("no reader found")
    return redirect('/')


@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect(url_for('index'))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    app.run(debug=True)
