from app import app
from flask import render_template, jsonify, request, flash, url_for, session, redirect
from apscheduler.schedulers.background import BackgroundScheduler

# checks if account is valid, this should be something more secure
def is_valid_account(password):
    return True

# get_refresh_predictions - getting static predictions
@app.route("/refresh", methods = ["GET", "POST"])
def refresh():
    if request.method == "POST":
        static_predictions, realtime_predictions = app.config["backend"].get_refresh_predictions()
        # TODO pass predictions correctly to the frontend UI
        return redirect("/home")

# get_realtime_predictions
# TODO edit the frontend UI To correctly recieve these
@app.route('/refresh_realtime') 
def refresh_realtime():
    realtime_predictions = app.config["backend"].get_realtime_predictions()
    return jsonify({"live_arrivals": realtime_predictions})

# Home Screen
@app.route("/home")
def home():    
    user_auth = session.get("auth", None)
    print(user_auth)
    if user_auth:
        static_predictions, realtime_predictions = app.config["backend"].get_refresh_predictions()
        # TODO pass this correctly to home
        return render_template("home.html", queue_lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    else:
        return redirect("/")

# Site settings
@app.route("/settings")
def settings():
    if session.get("auth", None):
        return render_template("settings.html")
    else: 
        return redirect("/")

## Login Screen
@app.route("/", methods = ["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        password = request.form.get("password")
        if is_valid_account(password):
            session["auth"] = True
            return redirect("home")
        else:
            return render_template("login.html", optional_error_msg = "Error - user account not recognised")            
    return render_template("login.html", optional_error_msg = "")
    
# automatically updates the realtime refresh every 10 secs
sched = BackgroundScheduler(daemon=True)
sched.add_job(refresh_realtime,'interval', seconds = 10)
sched.start()