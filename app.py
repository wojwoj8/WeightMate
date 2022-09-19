from flask import Flask, render_template, redirect, request, session, flash
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from addfunc import login_required, startform_required

from datetime import datetime, timedelta


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#user database
udb = SQL("sqlite:///users.db")


@app.route("/")
@login_required
@startform_required
def index():

    weight = udb.execute("SELECT weight FROM measurements WHERE user_id = ?", session["user_id"])
    data = udb.execute("SELECT weight,date FROM measurements WHERE user_id = ?", session["user_id"])
    data2 = udb.execute("SELECT goal,rate,bmr,tdee,height,age,gender,activity,username FROM users WHERE id = ?", session["user_id"])

    if len(weight) < 1:
        #print(weight)
        return redirect("/getstarted")

    else:
        rate = data2[0]["rate"]
        tdee = data2[0]["tdee"]
        weig = data[-1]["weight"]
        goal = data2[0]["goal"]
        date = data[-1]["date"]
        age = data2[0]["age"]
        gend = data2[0]["gender"]
        sport = data2[0]["activity"]
        height = data2[0]["height"]
        uname = data2[0]["username"]

        if gend == "Male":
            bmr = 10 * weig + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weig + 6.25 * height - 5 * age - 161
        bmr = round(bmr)

        if sport == "Sedentary/No excercise":
            tdee = bmr * 1.2
        elif sport == "Light exercise 1-3 times per week":
            tdee = bmr * 1.4
        elif sport == "Light exercise 4-6 times per week":
            tdee = bmr * 1.5
        elif sport == "Intense excercise 3-4 times per week":
            tdee = bmr * 1.6
        elif sport == "Intense excercise 4-6 times per week":
            tdee = bmr * 1.7
        elif sport == "Very intense daily excercise or physical job":
            tdee = bmr * 1.9

        tdee = round(tdee)
        #print(data)

        #print(weig)
        #update bmr and tdee
        udb.execute("UPDATE users SET bmr = ?, tdee = ? WHERE id = ?",bmr, tdee, session["user_id"])
        #chart

        chart_data = udb.execute("SELECT weight, date FROM measurements WHERE user_id = ?  ORDER BY date ASC", session["user_id"])

        #print(chart_data)
        labels = [chart_data[i]["date"] for i in range(len(chart_data))]
        values = [chart_data[i]["weight"] for i in range(len(chart_data))]
        #print(labels)
        #print(values)


        if rate != 0:
            tempo = (goal - weig) / rate
            if tempo < 0:
                tempo = tempo * -1
            tempo = tempo * 7
            tempo = round(tempo)
            #print(tempo)

            tdee = int(tdee)
            rate = float(rate)
            calories = 7000 / 7 * rate
            if (goal - weig) < 0:
                calories = tdee - calories
            else:
                calories = tdee + calories
            calories = int(calories)
            #print(calories)
            date = date[0:10]
            #print(date)
            #print(f" date = {date[0:10]}")
            date_1 = datetime.strptime(date, "%Y-%m-%d")
            end_date = date_1 + timedelta(days=tempo)
            #end_date = end_date[0:10]
            end_date = str(end_date)[0:10]
            #print(end_date)
            #print(objDate)

            return render_template("index.html", calories=calories, end_date=end_date, goal=goal, tdee=tdee, labels=labels, values=values, uname=uname)

        else:
            calories = tdee
            return render_template("index.html", calories=calories, tdee=tdee, labels=labels, values=values, uname=uname)



@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id") is not None:
        return redirect("/")

    if request.method == "POST":
        #Validation
        if not request.form.get("username"):
            return render_template("register.html")
        elif not request.form.get("password"):
            return render_template("register.html")
        elif not request.form.get("password"):
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html")
        uname = request.form.get("username")
        rows = udb.execute("SELECT * FROM users WHERE username = ?", uname)
        if len(rows) != 0:
            return render_template("register.html", uname=uname)

        hpw = generate_password_hash(request.form.get("password"))
        udb.execute("INSERT INTO users (username, hash) VALUES (?, ?)", uname, hpw)
        id = udb.execute("SELECT id FROM users WHERE (username = ?)", uname)
        session["user_age"] = None
        session["user_id"] = id[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id") is not None:
        return redirect("/")

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html")
        elif not request.form.get("password"):
            return render_template("login.html")

        rows = udb.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            #for printing error on page
            x=1
            return render_template("login.html", x=x)

        #id of logged user
        session["user_id"] = rows[0]["id"]
        session["age"] = rows[0]["age"]

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/notlogged")
def notlogged():
    if session.get("user_id") is None:
        return render_template("notlogged.html")
    else:
        return redirect("/")

@app.route("/getstarted", methods=["GET", "POST"])
@login_required
def getstarted():
    activity= [
            "Sedentary/No excercise",
            "Light exercise 1-3 times per week",
            "Light exercise 4-6 times per week",
            "Intense excercise 3-4 times per week",
            "Intense excercise 4-6 times per week",
            "Very intense daily excercise or physical job"
        ]
    gender=[
        "Male",
        "Female"
    ]
    weight = udb.execute("SELECT weight FROM measurements WHERE user_id = ?", session["user_id"])

    if request.method == "GET":
        if len(weight) < 1:
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender)

        else: #- here you already started or smthng liek that
            return redirect("/")
    else:
            #write validation later in js
        age = request.form.get("age")
        height = request.form.get("height")
        weig = request.form.get("weight")
        gend = request.form.get("gender")
        goal = request.form.get("goal")
        rate = request.form.get("rate")

        sport = request.form.get("Activities")

        rate = float(rate)
        rate = round(rate,1)

        weig = float(weig)
        weig = round(weig,1)

        goal = float(goal)
        goal = round(goal,1)

        height = int(height)
        age = int(age)

        if not age or int(age) not in range(10,110):
            error = "Incorrect age"
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)

        if not height or int(height) not in range(50,300):
            error = "Incorrect height"
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)

        if not weig or weig < 20 or weig > 800:
            error = "Incorrect weight"
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)

        if gend not in gender:
            error = "You must select your gender"
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)

        if sport not in activity:
            error = "You must select your activity"
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)

        if not goal or goal < 20 or goal > 800:
            error = "Incorrect goal weight"
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)

        if rate < 0 or rate > 1:
            error = "Rate has to be between 0 and 1"
            print(rate)
            return render_template("getstarted.html", weight=weight, activity=activity, gender=gender, error=error)


        if gend == "Male":
            bmr = 10 * weig + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weig + 6.25 * height - 5 * age - 161
        bmr = round(bmr)
        #tdee = bmr * activity

        if sport == "Sedentary/No excercise":
            tdee = bmr * 1.2
        elif sport == "Light exercise 1-3 times per week":
            tdee = bmr * 1.4
        elif sport == "Light exercise 4-6 times per week":
            tdee = bmr * 1.5
        elif sport == "Intense excercise 3-4 times per week":
            tdee = bmr * 1.6
        elif sport == "Intense excercise 4-6 times per week":
            tdee = bmr * 1.7
        elif sport == "Very intense daily excercise or physical job":
            tdee = bmr * 1.9

        tdee = round(tdee)
        #print(tdee)
        #update data in db
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        udb.execute("INSERT INTO measurements (user_id, weight, date) VALUES (?, ?, ?)",
                     session["user_id"], weig, dt_string)

        udb.execute("UPDATE users SET age = ? , height = ?, gender = ?, activity = ?, bmr = ?, tdee = ?, goal = ?, rate = ?  WHERE id = ?",
                     age, height, gend, sport, bmr, tdee, goal, rate, session["user_id"])

        session["age"] = age
        #transition to second form
        return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
@login_required
@startform_required
def profile():
    x = udb.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    x = x[0]["username"]

    return render_template("profile.html", x=x)

@app.route("/addmeas", methods=["GET", "POST"])
@login_required
@startform_required
def addmeas():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    x = udb.execute("SELECT * FROM measurements WHERE user_id = ? AND date = ?", session["user_id"], dt_string)
    list = ['weight', 'neck', 'chest', 'left_arm', 'right_arm', 'waist',
                'abdomen', 'hips', 'left_thigh', 'right_thigh', 'left_calf', 'right_calf', 'date']

    if request.method == "GET":
        if len(x) == 0:
            x = dict.fromkeys(list, None)
            x = [x]
        return render_template("addmeas.html", x=x, date=dt_string)
    else:
        #wow
        new_list = []
        def test(measure):
            measure = request.form.get(f"{measure}")
            if measure != None or measure != '':
                try:
                    measure = float(measure)
                    measure = round(measure,1)
                    return measure
                except ValueError:
                    pass
                except TypeError:
                    pass


        date = request.form.get("date")
        regex = datetime.strptime
        try:
            assert regex(date, '%Y-%m-%d')
        except ValueError:
            flash("Date format is YYYY-MM-DD")
            return redirect("/addmeas")
        #now = datetime.now()
        #dt_string = now.strftime("%Y-%m-%d")
        date_ch = udb.execute("SELECT date FROM measurements WHERE user_id = ? AND date = ?", session["user_id"], date)

        for i in list:
            x = test(i)
            new_list.append(x)

        what = zip(list, new_list)
        newdict = dict(what)

        print(newdict)
        if newdict["weight"] == None or newdict["weight"] < 20 or newdict["weight"] > 800:
            flash("Incorrect weight")
            return redirect("/addmeas")


        #if this date in database update, else insert
        if len(date_ch) == 1:
            udb.execute("UPDATE measurements SET weight = ?, neck = ?, chest = ?, left_arm = ?, right_arm = ?, waist = ?, abdomen = ?, hips = ?, left_thigh = ?, right_thigh = ?, left_calf = ?, right_calf = ? WHERE user_id = ? AND date = ?",
             newdict['weight'], newdict['neck'], newdict['chest'], newdict['left_arm'], newdict['right_arm'], newdict['waist'], newdict['abdomen'], newdict['hips'], newdict['left_thigh'], newdict['right_thigh'], newdict['left_calf'], newdict['right_calf'], session["user_id"], date)
            msg = "Operation was successful"
            return redirect("/")
        else:
            udb.execute("INSERT INTO measurements (user_id, weight, date, neck, chest, left_arm, right_arm, waist, abdomen, hips, left_thigh, right_thigh, left_calf, right_calf) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
             session["user_id"], newdict["weight"], date, newdict["neck"], newdict['chest'], newdict['left_arm'], newdict['right_arm'], newdict['waist'], newdict['abdomen'], newdict['hips'], newdict['left_thigh'], newdict['right_thigh'], newdict['left_calf'], newdict['right_calf'])
            return redirect("/")

@app.route("/checkdata", methods=["GET", "POST"])
@login_required
@startform_required
def checkdata():
    data = udb.execute("SELECT * FROM measurements WHERE user_id = ? ORDER BY date", session["user_id"])
    for d in data:
        d.pop("user_id")

    return render_template("checkdata.html", data=data)

@app.route("/modprof", methods=["GET", "POST"])
@login_required
@startform_required
def modprof():
    gender=[
        "Male",
        "Female"
    ]
    data = udb.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    if request.method == "GET":
        return render_template("modprof.html", data=data, gender=gender)
    else:
        uname = request.form.get("username")
        pwd = request.form.get("password")
        conf = request.form.get("confirmation")
        age = request.form.get("age")
        height = request.form.get("height")
        gend = request.form.get("gender")

        print(f"pwd = {pwd}")
        print(f"confirm = {conf}")
        if not uname:
            error = "You have to type username"
            return render_template("modprof.html", data=data, gender=gender, error=error)
        if not age or int(age) not in range(10,110):
            error = "Age must be in range 10 - 110"
            return render_template("modprof.html", data=data, gender=gender, error=error)
        age = int(age)

        if not height or int(height) not in range(50,300):
            error = "Hight must be in range 50 - 300"
            return render_template("modprof.html", data=data, gender=gender, error=error)

        height = int(height)

        if gend not in gender:
            error = "You can only chose between male and female"
            return render_template("modprof.html", data=data, gender=gender, error=error)

        #first update data which is easy to change
        udb.execute("UPDATE users SET age = ?, height = ?, gender = ? WHERE id = ?", age, height, gend, session["user_id"])

        #uname and password
        #if change username
        if uname != data[0]["username"]:
            rows = udb.execute("SELECT username FROM users WHERE username = ?", uname)
            #if username exists
            if len(rows) != 0:
                error = "This username already exists"
                return render_template("modprof.html", data=data, gender=gender, error=error)
            else:
                udb.execute("UPDATE users SET username = ? WHERE id = ?", uname, session["user_id"])

        #password change
        if request.form.get("password") != request.form.get("confirmation"):
            error = "Password and Confirm Password must be the same"
            return render_template("modprof.html", data=data, gender=gender, error=error)
        elif not pwd:
            return redirect("/profile")
        elif not conf:
            return redirect("/profile")
        else:
            hpw = generate_password_hash(pwd)
            udb.execute("UPDATE users SET hash = ? WHERE id = ?", hpw, session["user_id"])

    return redirect("/profile")

@app.route("/changoal", methods=["GET", "POST"])
@login_required
@startform_required
def changoal():
    activity= [
            "Sedentary/No excercise",
            "Light exercise 1-3 times per week",
            "Light exercise 4-6 times per week",
            "Intense excercise 3-4 times per week",
            "Intense excercise 4-6 times per week",
            "Very intense daily excercise or physical job"
        ]
    data = udb.execute("SELECT goal,rate,activity FROM users WHERE id = ?", session["user_id"])
    if request.method == "GET":

        return render_template("changoal.html", data=data, activity=activity)


    else:
        goal = request.form.get("goal")
        rate = request.form.get("rate")
        sport = request.form.get("activity")

        try:
            rate = float(rate)
            rate = round(rate,1)
            goal = float(goal)
            goal = round(goal,1)

        except ValueError:
            flash("Value must be a digit")
            return render_template("changoal.html", data=data, activity=activity)

        if not goal or goal < 20 or goal > 800:
            flash("Your targer weight must be between 20 - 800 kg")
            return render_template("changoal.html", data=data, activity=activity)

        elif rate < 0 or rate > 1:
            flash("Rate must be between 0 - 1 kg/week, more is unhealthy")
            return render_template("changoal.html", data=data, activity=activity)

        elif sport not in activity:
            flash("You must select your activity")
            return render_template("changoal.html", data=data, activity=activity)

        else:
            udb.execute("UPDATE users SET goal = ?, rate = ?, activity = ? WHERE id = ?", goal, rate, sport, session["user_id"])
            flash("Goal changed successfully")
            return redirect("/profile")