from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session

from flask import url_for, redirect
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CSRFProtect(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        print(username)
    custome_cookie = request.cookies.get('custome_cookie', 'nada_encontrado')
    print(custome_cookie)
    return render_template('Login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['user']
    return '<h1>hola</h1>'

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop['username']
    return redirect(url_for('index'))


@app.route('/cookie', methods = ['GET', 'POST'])
def cookie():
    reponse = make_response( render_template('cookie.html'))
    reponse.set_cookie('custome_cookie', 'Emmanuel')
    return reponse


if __name__ == '__main__':
  app.run(debug = True, port = 9600 )
