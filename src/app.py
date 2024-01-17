from flask import make_response, redirect, render_template, request, session, url_for, jsonify
from conf import app

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

import api.routes
from api.user import UserModel, UserSchema

@app.route("/login", methods = ['POST'])
def user_login():
    # login?
    user_data = UserModel.query.filter(UserModel.uname == request.form['uname']).first() or None
    if user_data is None:
        return jsonify(message = "User not found"), 404
    else:
        print(len(user_data.upass), generate_password_hash(request.form['upass']))
        if check_password_hash(user_data.upass, request.form['upass']):
            session['id'] = int(hashlib.sha1(user_data.uname.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
            return jsonify(message = "Logged in successfully!"), 200
        else:
            return jsonify(message = "Wrong password!"), 200

@app.route("/logout", methods = ['GET'])
def user_logout():
    if session.get('id'):
        session.pop('id', None)
        return jsonify(message = "Logged out!"), 200
    else:
        return jsonify(message = "No user is currently logged in!"), 409

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(message = "The requested resource could not be found.", error = str(e)), 404

# MAIN
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)