import sqlite3,os,Login,Clubs,Events

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

@app.route('/register_for_event', methods=['POST'])
def register_for_event():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    
    if request.method == 'POST':
        event_id = request.form['event_id']
        user_id = Login.get_user_id(username)
        
        error_message = Events.register_for_event(event_id, user_id)
        
        if error_message:
            return render_template('event_registration_error.html', error_message=error_message, roleCheck=roleCheck)
        else:
            return render_template('successful_registration.html')

    
@app.route('/your_club')
def your_club():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    user_ID = Login.get_user_id(username)
    if Clubs.verify_clubs_coordinated(user_ID) == 0:
        return redirect(url_for('coordinator_noclub'))
    else:
        return render_template('coordinator_page.html', roleCheck=roleCheck, username=username)
    
@app.route('/memberships')
def memberships():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    userID = Login.get_user_id(username)
    joinedList = []
    for item in Clubs.user_views_memberships(userID):
        joinedList.append(item)
    return render_template('memberships.html', joinedList=joinedList, roleCheck=roleCheck, username=username)

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
    UserID = Login.get_user_id(username)
    pending_memberships = []
    for item in Clubs.coordinator_view_club_pending_memberships(UserID):
        pending_memberships.append(item)
    return render_template('pending_members.html', pending_memberships=pending_memberships, roleCheck=roleCheck, username=username)

@app.route('/coordinator_accept_club_membership', methods=['POST'])
def coordinator_accept_club_membership():
    if request.method == 'POST':
        membership_id = request.form.get('membership_id')
        Clubs.update_membership_status(membership_id)
        return redirect(request.referrer or '/')
    
@app.route('/coordinator_reject_club_membership', methods=['POST'])
def coordinator_reject_club_membership():
    if request.method == 'POST':
        membership_id = request.form.get('membership_id')
        Clubs.reject_club_membership(membership_id)
        # Redirect back to the same page (refresh)
        return redirect(request.referrer or '/')
    
@app.route('/add_membership', methods=['POST'])
def add_membership():
    if request.method == 'POST':
        sport_name = request.form.get('sportName')
        username = session.get('username')  # Get the username from the session

        if username:
            UserID = Login.get_user_id(username)
            ClubID = Clubs.get_club_id_using_sport_name(sport_name)

            if ClubID is not None:  # Check if ClubID is valid
                try:
                    Clubs.club_registration(UserID, ClubID)
                    flash(f"Membership added successfully for {sport_name}.", "success")
                except Exception as e:
                    flash(f"Failed to add membership for {sport_name}. Error: {str(e)}", "error")
            else:
                flash(f"Club ID not found for {sport_name}.", "error")
        else:
            flash("Username not found in session.", "error")

        return redirect('/memberships')

@app.route("/delete_club_membership/<int:membership_id>", methods=["POST"])
def delete_club_membership(membership_id):
    if request.method == "POST":
        membership_id = request.form['membership_id']
        Clubs.delete_club_membership(membership_id)
        return redirect(request.referrer or '/')
    


@app.route("/delete_event", methods=["POST"])
def delete_event():
    if request.method == "POST":
        eventID = request.form['eventID']
        Events.delete_event(eventID)
        return redirect('/coordinator_view_club_events')


    
@app.route('/club_successfully_joined')
def club_successfully_joined():
    return render_template('club_successfully_joined.html')

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
    event_registrations = Events.coordinator_view_event_registrations(UserID)
    return render_template('coordinator_view_event_registrations.html', event_registrations=event_registrations, UserID=UserID, roleCheck=roleCheck, username=username)

@app.route("/coordinator_view_pending_event_registrations")
def coordinator_view_pending_event_registrations():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    UserID = Login.get_user_id(username)
    pending_event_registrations = Events.coordinator_view_pending_event_registrations(UserID)
    return render_template("coordinator_view_pending_event_registrations.html", pending_event_registrations=pending_event_registrations, roleCheck=roleCheck, username=username)

@app.route('/coordinator_accept_event_registration', methods=['POST'])
def coordinator_accept_event_registration():
    if request.method == 'POST':
        registrationID = request.form.get('registrationID')
        Events.accept_event_registration(registrationID)
        return redirect(request.referrer or '/')

@app.route('/coordinator_reject_event_registration', methods=['POST'])
def coordinator_reject_event_registration():
    if request.method == 'POST':
        registrationID = request.form.get('registrationID')
        Events.reject_event_registration(registrationID)
        return redirect(request.referrer or '/')  

@app.route("/coordinator_create_event", methods=["GET", "POST"])
def coordinator_create_event():
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    CoordinatorID = Login.get_user_id(username)
    club_id = Clubs.get_ClubID(CoordinatorID)
    if request.method == "POST":
        username = session.get("username", "base")
        title = request.form.get("title")
        description = request.form.get("description")
        date_ = request.form.get("date")
        time_ = request.form.get("time")
        venue_name = request.form.get("venue_id")

        actual_venue_id = Events.get_VenueID_from_VenueName(venue_name)
        user_id = request.form.get("user_id")

        # Call the create_event function
        Events.create_event(club_id, title, description, date_, time_, actual_venue_id)
    # Render the create event form with club ID and user ID
    user_id = request.args.get("user_id")
    venues = Events.get_all_venues()

    return render_template("create_event.html", club_id=club_id, user_id=user_id, venues=venues)



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
        flash("User deleted", "success")
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

@app.route("/admin_clubs")
def admin_clubs():
    club_list = []
    for item in Clubs.pending_clubs():
        club_list.append(item)
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    return render_template("admin_clubs.html",club_list=club_list, roleCheck=roleCheck, username=username)

@app.route("/approve_club/<int:ClubID>", methods=["POST"])
def approve_club(ClubID):
    if request.method == "POST":
        Clubs.approve_club(ClubID)
        return redirect(url_for("admin_clubs"))
    else:
        return redirect(url_for("admin_clubs"))

@app.route("/reject_club/<int:ClubID>", methods=["POST"])
def reject_club(ClubID):
    if request.method == "POST":
        Clubs.reject_club(ClubID)
        return redirect(url_for("admin_clubs"))
    else:
        return redirect(url_for("admin_clubs"))

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
    
@app.route("/coordinator_noclub", methods=["POST", "GET"])
def coordinator_noclub():
    message = None
    roleCheck = session.get("roleCheck", 0)
    username = session.get("username", "base")
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        description = request.form["description"]
        user_ID = Login.get_user_id(username)
        message = Clubs.creating_club(name,user_ID,description)
    return render_template("coordinator_noclub.html",roleCheck=roleCheck,message=message,username=username)

#allows me to go through clubList
@app.template_filter('enumerate')
def jinja2_enumerate(iterable):
    return enumerate(iterable)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
