import sqlite3, os,Login,Clubs,Events

from flask import Flask, redirect, url_for, render_template, request, session, flash

# importing real time to create permanent session for perios of time
from datetime import timedelta
app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
miniwebsite_dir = os.path.join(current_dir, '..')
database_path = os.path.join(miniwebsite_dir, 'MiniWebsite', 'MiniEpic.db')
app.config['DATABASE'] = database_path

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)

@app.route("/")
@app.route("/home")
def home():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("home.html", roleCheck=roleCheck, username=username)


@app.route("/login", methods=["POST", "GET"])
def login():
    error_message = None
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]
        if Login.validate_user(username, password):
            roleCheck = Login.login(username, password)
            if roleCheck is not None:
                session["username"] = username
                session["roleCheck"] = roleCheck
                return redirect(url_for("home"))
        else:
            error_message = "Invalid username or password. Please try again."
    return render_template("login.html", error_message=error_message)


@app.route("/register", methods=["POST", "GET"])
def register():
    error_message2 = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        phone = request.form["phone"]

        if Login.verify_username(username) == False:
            error_message2 = "Username Taken"
        elif Login.validate_reg(email) == False:
          error_message2 = "Email Taken"
        elif Login.is_valid_email(email) == False:
            error_message2 = "Email invalid"
        elif Login.verify_phone(phone) == False:
            error_message2 = "Phone Number invalid"
        else:
            roleCheck = Login.create_account(username,password,name,surname,email,phone)
            session["username"] = username
            session["roleCheck"] = roleCheck
            return redirect(url_for("home"))
    return render_template("register.html", error_message2=error_message2)


@app.route("/logout")
def logout():
    if "username" in session:
        user = session["username"]
        flash(f"You have been logged out, {user}", "info")
        session.pop("username", None)
        session.pop("roleCheck", None)
    return redirect(url_for("home"))


@app.route("/clubs")
def clubs():
    clubList = []
    for item in Clubs.user_view_clubs():
        clubList.append(item)
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("clubs.html", clubList=clubList, roleCheck=roleCheck, username=username)


@app.route("/events")
def display_events_page():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("events.html", roleCheck=roleCheck, username=username)

@app.route('/view_events')
def view_events_route():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    events = Events.view_events()
    return render_template('view_events.html', events=events, roleCheck=roleCheck, username=username)


@app.route('/user_views_event_registrations')
def user_views_event_registrations():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    userID = Login.get_user_id(username)
    registered_events = Events.fetch_user_event_registrations(userID)
    return render_template('view_event_registrations.html', event_registrations=registered_events, userID=userID, roleCheck=roleCheck, username=username)

@app.route('/register_event', methods=['POST'])
def register_event():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    if request.method == 'POST':
        event_id = request.form['event_id']
        user_id = request.form['user_id']
        
        Events.register_for_event(event_id, user_id)
    
        return render_template('successful_registration.html', roleCheck=roleCheck, username=username)
    
@app.route('/your_club')
def your_club():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template('coordinator_page.html', roleCheck=roleCheck, username=username)

@app.route('/coordinator_view_club_memberships')
def coordinator_view_club_memberships():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    userID = Login.get_user_id(username)
    memberships = []
    for item in Clubs.coordinator_view_club_memberships(userID):
        memberships.append(item)
    return render_template('club_memberships.html', memberships=memberships, roleCheck=roleCheck, username=username)

@app.route('/coordinator_view_club_pending_memberships')
def coordinator_view_club_pending_memberships():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    userID = Login.get_user_id(username)
    pending_memberships = []
    for item in Clubs.coordinator_view_club_pending_memberships(userID):
        pending_memberships.append(item)
    return render_template('pending_members.html', pending_memberships=pending_memberships, roleCheck=roleCheck, username=username)


@app.route('/coordinator_view_club_events')
def coordinator_view_club_events():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    UserID = Login.get_user_id(username)
    club_events = []
    for item in Events.coordinator_view_events(UserID):
        club_events.append(item)
    return render_template('view_club_events.html', club_events=club_events, UserID=UserID, roleCheck=roleCheck, username=username)

@app.route('/coordinator_view_event_registrations')
def coordinator_view_event_registrations():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    UserID = Login.get_user_id(username)
    event_registrations = []
    for item in Events.coordinator_view_event_registrations(UserID):
        event_registrations.append(item)
        return render_template('coordinator_view_event_registrations.html', event_registrations=event_registrations, UserID=UserID, roleCheck=roleCheck, username=username)

@app.route("/memberships")
def memberships():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("memberships.html",  roleCheck=roleCheck, username=username)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    user_id = Login.get_user_id(username)
    temp_list = ["User ID: ", "Full Name: ", "Username: ", "Email: ", "Phone Number: ", "Role: ","Approval Status: ", "Account Created: "]
    temp_list2 = []
    for item in Login.admin_view_user(user_id):
        temp_list2.append(item)
    user_details = [item1 + str(item2) for item1, item2 in zip(temp_list, temp_list2)]
    update_message = None
    update_message2 = None
    error_message = None

    if request.method == "POST":
        if "phone" in request.form:
            phone = request.form["phone"]
            Login.update_number(user_id, phone)
            update_message = "Phone Number Updated"

        elif "old_password" in request.form and "new_password" in request.form:
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            user_id = Login.get_user_id(username)
            result = Login.update_password(user_id, old_password, new_password)
            if result == "valid":
                update_message2 = "Password Updated"
            elif result == "invalid":
                error_message = "Invalid Password"

    return render_template("profile.html", roleCheck=roleCheck, username=username,update_message2=update_message2, update_message=update_message, error_message=error_message,user_details=user_details)

@app.route("/users")
def users():
    user_list = []
    for item in Login.admin_view_accounts():
        user_list.append(item)
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("users.html", user_list=user_list, roleCheck=roleCheck, username=username)

@app.route("/promote_user/<int:user_id>", methods=["POST"])
def promote_user(user_id):
    if request.method == "POST":
        Login.promote_user(user_id)
        flash("User promoted successfully", "success")
        return redirect(url_for("users"))
    else:
        flash("Invalid request method", "error")
        return redirect(url_for("users"))
    
@app.route("/approve_user/<int:user_id>", methods=["POST"])
def approve_user(user_id):
    if request.method == "POST":
        Login.approve_user(user_id)
        flash("User approved", "success")
        return redirect(url_for("users"))
    else:
        flash("Invalid", "error")
        return redirect(url_for("users"))

@app.route("/delete_account/<int:user_id>", methods=["POST"])
def delete_account(user_id):
    if request.method == "POST":
        Login.delete_account(user_id)
        flash("User approved", "success")
        return redirect(url_for("users"))
    else:
        flash("Invalid", "error")
        return redirect(url_for("users"))

@app.route("/coordinators")
def coordinators():
    coord_list = []
    for item in Login.view_coordinators():
        coord_list.append(item)
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("coordinators.html",coord_list=coord_list, roleCheck=roleCheck, username=username)
    

@app.route('/view_event_registrations', methods=['GET'])
def view_event_registrations():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("view_event_registrations.html", roleCheck=roleCheck, username=username)

@app.route("/advent")
def adminevent():
    events_list = []
    for item in Events.admin_view_events_pending():
        events_list.append(item)
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("advent.html",events_list=events_list, roleCheck=roleCheck, username=username)

@app.route("/approve_registration/<int:registration_id>", methods=["POST"])
def approve_registration(registration_id):
    if request.method == "POST":
        Events.approve_registration(registration_id)
        flash("Event approved", "success")
        return redirect(url_for("adminevent"))
    else:
        flash("Invalid", "error")
        return redirect(url_for("adminevent"))

#allows me to go through clubList
@app.template_filter('enumerate')
def jinja2_enumerate(iterable):
    return enumerate(iterable)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
