from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests
import jwt
from Cryptodome.PublicKey import RSA
from base64 import urlsafe_b64decode
import mysql.connector as mariadb
from random import choice as choose
import config


app = Flask(__name__)
#app.config.from_pyfile('config.py')
app.config.from_object(config.Dev())



mariadb_connection = mariadb.connect(user=app.config['DB_USER'], password=app.config['DB_PW'], host=app.config['DB_HOST'],database='quotes')
cursor = mariadb_connection.cursor()


client_id = app.config['COGNITO_CLIENT_ID']
redirect_uri = app.config['COGNITO_REDIRECT_URI']
verify_url = "https://cognito-idp.us-west-2.amazonaws.com/"+app.config['USER_POOL_ID']+"/.well-known/jwks.json"

@app.route('/auth')
def auth():
    url = app.config['AUTH_URL']
    code = request.args["code"]
    if code != None:
        myobj = {"grant_type":"authorization_code",
            "code":code,
            "client_id":client_id,
            "redirect_uri":redirect_uri}
        response = requests.post(url, data = myobj)
        verify = requests.get(verify_url)

        token = response.json()
        header = jwt.get_unverified_header(token["id_token"])
        kid = header['kid']
        alg = header['alg']

        modulus = None
        exponent = None
        for key in verify.json()["keys"]:
            if kid == key['kid']:
                modulus = key['n'] #Grab modulus and and convert to PEM format to be used as secret during decode
                exponent = key['e']

        if (modulus != None) and (exponent != None):
            modulus = modulus + '=' * (4 - len(modulus) % 4)
            i = int.from_bytes(urlsafe_b64decode(modulus),'big') #why big endian and urlsafe_b64decode (vs. b64decode)????
            j = int.from_bytes(urlsafe_b64decode(exponent),'big')
            key = RSA.construct((i,j))
            PEM = key.exportKey()

            decoded = jwt.decode(token["id_token"], PEM, audience=client_id, algorithms=alg)
            #Required attributes
            if 'cognito:username' in decoded:
                session['username']=decoded['cognito:username']
            else:
                return "Error: no username detected"
            #Optional Attributes
            if 'cognito:groups' in decoded:
                session['groups']=decoded['cognito:groups']
            return redirect(url_for('main'))
        else:
            return "Uh-oh an error has occurred!"


@app.route('/main')
def main():
    try:
        user = session['username']
        return render_template("main.html", username=session['username'])
    except:
        return redirect(url_for('index'))

@app.route('/edit')
def edit():
    try:
        user = session['username']
        cursor.execute("SELECT quotes, attributed, qid FROM quotes WHERE user=%s", (user,))
        quotes = cursor.fetchall()
        return render_template("edit.html", quotes=quotes)
    except:
        pass


@app.route('/editrefresh')
def editreferesh():
    try:
        user = session['username']
        cursor.execute("SELECT quotes, attributed, qid FROM quotes WHERE user=%s", (user,))
        quotes = cursor.fetchall()
        return render_template("edit-window-edit-container.html", quotes=quotes)
    except:
        pass


@app.route('/submitquote', methods=['POST'])
def submitQuote():
    data = request.get_json(force=True,silent=False);
    cursor.execute("INSERT INTO quotes (user, quotes, attributed) values (%s,%s,%s)", (session['username'],data['q'],data['a']))
    mariadb_connection.commit()
    return data


@app.route('/deletequote', methods=['POST'])
def deleteQuote():
    data = request.get_json(force=True,silent=False);
    qid = data['qid']
    cursor.execute("SELECT user FROM quotes WHERE qid=%s", (qid,))
    user = cursor.fetchall()
    if user[0][0] == session['username']:
        cursor.execute("DELETE FROM quotes WHERE qid=%s", (qid,))
        mariadb_connection.commit()
        return "Delete succeeded."
    else:
        return "Delete failed. You are not authorized to delete this quote."
    return "Other"




@app.route('/newquote')
def newQuote():
    if session['username'] != None:
        user = session['username']
        cursor.execute("SELECT * FROM quotes WHERE user=%s", (user,))
        quotes = cursor.fetchall()
        q = choose(quotes)
        return jsonify(quote=q[2],source=q[3])
    else:
        return jsonify("None")




@app.route('/')
def index():
    return render_template("index.html",LOGIN_URL=app.config['LOGIN_URL'])


if __name__ == "__main__":
    if app.config['DEBUG'] == True:
        app.run(ssl_context='adhoc')
    else:
        app.run()
