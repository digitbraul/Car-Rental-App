from flask import redirect, render_template, request, session, url_for
from conf import app
import hashlib

# Routing handlers for web app (Jinja for server-side templating and jQuery in target pages)
@app.route("/")
def home():
    return render_template('home.html')

# don't use
@app.route("/api/add_cars", methods = ['GET', 'POST'])
def add_car():
    if not session.get('logged-in'):
        return redirect(url_for('login.html'))
    
    # TODO : remove this and only keep the dashboard, it'll send requests via jQuery for the API to validate them


@app.route("/admin", methods = ['GET', 'POST'])
def admin_login():
    if session.get('logged-in'):
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        # Read the values posted from the form
        _uname = request.form['username']
        _upass = request.form['userpass']

        # Validate input
        if not (_uname and _upass):
            return render_template('login.html', msg="Please check input!")

        # Fetch user and pass from database TODO: don't
        acc = fetch_user(uname=_uname, password=_upass)
        if acc:
            session['logged-in'] = True
            session['id'] = int(hashlib.sha1(acc['username'].encode("utf-8")).hexdigest(), 16) % (10 ** 8)
            msg = "Logged in successfully!"
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', msg="Wrong username or password!")

@app.route('/logout')
def logout():
    session.pop('logged-in', None)
    session.pop('id', None)
    return redirect(url_for('admin_login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged-in'):
        return redirect(url_for('admin_login'))
    
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# MAIN
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)