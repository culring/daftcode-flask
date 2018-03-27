from functools import wraps
from random import random
from flask import Flask, request, redirect, url_for, make_response, render_template
from flask.json import jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'Akwarysta69'
app.config['BASIC_AUTH_PASSWORD'] = 'J3si07r'

basic_auth = BasicAuth(app)

cookie = 0
fishes = dict()
counter = 1


def check_is_logged_in():
    cookie_secret = request.cookies.get('cookie_secret')
    return cookie != 0 or cookie_secret == cookie


def protected(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not check_is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return wrap


@app.route('/')
def main():
    return 'Hello, World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if check_is_logged_in():
        return redirect(url_for('hello'))

    if request.method == 'GET':
        return ''' 
               <style type="text/css">
               kek { padding-left: 4em; } /* Firefox ignores first declaration for some reason */
               tab1 { padding-left: 4em; }
               </style>

               <form action = "" method = "post">
                   <p>login:</p>
                   <p><input type = text name = login></p>
                   <p>password:</p>
                   <p><input type = text name = pass></p>
                   <p><input type = submit value = Login></p>
               </form>
           '''

    if "test" in request.args:
        username, password = request.form['login'], request.form['pass']
    else:
        js = request.get_json()
        username, password = js['login'], js['pass']

    if not basic_auth.check_credentials(username, password):
        return "DENIED", 401

    global cookie
    cookie = str(random())

    resp = make_response('logged in')
    resp.set_cookie('cookie_secret', cookie)
    return resp


@app.route('/logout', methods=['GET', 'POST'])
@protected
def logout():
    resp = redirect(url_for('main'))
    resp.set_cookie('cookie_secret', '-')
    global cookie
    cookie = 0
    return resp


@app.route('/hello')
@protected
def hello():
    return render_template('hello.html', name=app.config['BASIC_AUTH_USERNAME'])


@app.route('/fishes', methods=['GET', 'POST'])
@protected
def happy():
    if request.method == 'POST':
        new_fish = dict(request.get_json())
        global fishes, counter
        fishes[counter] = new_fish
        counter += 1
        return redirect(url_for('carla', fish_id=counter-1))
    elif request.method == 'GET':
        print(fishes)
        return jsonify(fishes)


@app.route('/fishes/<fish_id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
@protected
def carla(fish_id):
    global fishes
    fish_id = int(fish_id)
    if fish_id not in fishes:
        return f"fish with id {fish_id} does not exist", 400

    if request.method == 'GET':
        return jsonify(fishes[fish_id])
    elif request.method == 'DELETE':
        fishes.pop(fish_id)
        return f'deleted fish with id {fish_id}'
    elif request.method == 'PUT':
        fishes[fish_id] = dict(request.get_json())
        return f'put fish with id {fish_id}'
    elif request.method == 'PATCH':
        patch = dict(request.get_json())
        for key, value in patch.items():
            fishes[fish_id][key] = value
        return f'patched fish with id {fish_id}'


@app.route("/my/reset", methods=['DELETE'])
@protected
def reset():
    global fishes, counter
    fishes = dict()
    counter = 1
    return 'data reset'


if __name__ == '__main__':
    app.run(debug=True)
