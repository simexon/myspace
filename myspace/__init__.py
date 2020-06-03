from flask import Flask, redirect, url_for, request, render_template, session, escape, session
import sqlite3, bcrypt
app = Flask(__name__)
app.secret_key = 'secretString'

@app.route('/<name>')
def urls(name):
    if (name == 'home'):
        name = 'index'

    if session['login']:
        return render_template(name + '.html', logged_in = session['login'], Full_name = session['Full_name'], username = session['username'])
    else:
        return render_template(name + '.html')

def urls():
    if session['login']:
        return render_template('index.html', logged_in = session['login'], Full_name = session['Full_name'], username = session['username'])
    else:   
        return render_template('index.html')
app.add_url_rule('/', '/home', urls)

#Existing user login
@app.route('/login', methods = ['POST'])
def login():
    if (request.method == 'POST'):
        loginUserName = validate(request.form['loginUsername'])
        loginPassword = (request.form['loginPassword']).strip()
    try:
        with sqlite3.connect("myspace.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT `username`, `password`, `Full_name` from user_accounts where username = ?", (loginUserName, ))
            records = cur.fetchone()
            if records:
                #check for password
                if checkHashePwd(loginPassword.encode(), records[1]):
                    msg =  "Hello "  + records[2]
                    session['login'] = True
                    session['username'] = records[0]
                    session['Full_name'] = records[2]
                    print('Session Data' + session['Full_name'])
                else:
                    msg = "Sign in Failed: Invalid Password"    
            else:
                msg = "User Account not found"

    except sqlite3.Error as err:
        print(str(err))
        msg = 'Sign in error. Error code: 520'
    finally:
        if session['login']:
            return render_template("index.html", msg = msg, logged_in = session['login'], Full_name = session['Full_name'], username = session['username'] )
        return render_template("index.html", msg = msg)
        conn.close()

#create a new user account
@app.route('/createAcc', methods = ['POST'])
def crtAcc():
    #return redirect(url_for('social'))
    if (request.method == 'POST'):
        regFullName = validate(request.form['regFullName'])
        regEmail = validate(request.form['regEmail'])
        regUsername = validate(request.form['regUsername'])
        regPassword = (request.form['regPassword']).strip()
        regRepeatPassword = (request.form['regRepeatPassword']).strip()
        try:
            if (regPassword == regRepeatPassword):
                regPassword = hashpwd(regPassword)
                with sqlite3.connect("myspace.db") as conn:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO user_accounts (`Full_name`, `username`, `email`, `password`) \
                        VALUES (?, ?, ?, ?)", (regFullName, regUsername, regEmail, regPassword) )
                    conn.commit()
                    msg = "Signed Up Succcessfully"
            else:
                msg = "Passwords Mismatch. Try again"

        except sqlite3.Error as err:
            conn.rollback()
            if str(err) == "UNIQUE constraint failed: user_accounts.email":
                msg = "Error in Signup: Email already used by another user"
            elif str(err) == "UNIQUE constraint failed: user_accounts.username":
                msg = "Error in Signup: Username unavailable. Please enter a different username"
            else:
                print(str(err))
                msg = 'Sign up error. Error code: 520'
        finally:
            return render_template("index.html", msg = msg)
            conn.close()

@app.route('/createPost')
def createPost():
    if session['login']:
        return render_template("createPost.html", logged_in = session['login'], Full_name = session['Full_name'], username = session['username'])
    return redirect(url_for('/home'))

@app.route('/signOut')
def signOut():
    session['login'] = False
    session.pop('Full_name', None)
    session.pop('username', None)
    return redirect(url_for('/home'))

def validate(string):
    #used to sanitize user inputs 
    return escape(string.strip())

def hashpwd(pwd):
    salt = bcrypt.gensalt()
    b = pwd.encode() # I just added this line
    return bcrypt.hashpw(b, salt)

def checkHashePwd(Userpwd, databasePwd):
    return bcrypt.checkpw(Userpwd, databasePwd)

if __name__ == '__main__':
   app.run(debug = False, host='0.0.0.0')
   #app.run(debug = True)