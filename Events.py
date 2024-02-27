import sqlite3,Login


def connect_to_database():
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    return conn, cursor


# temp function to verify whether someone is a coordinator
def is_coordinator(user_id):
    conn, cursor = connect_to_database()
    cursor.execute("SELECT Role FROM Users WHERE UserID=?", (user_id,))
    role = cursor.fetchone()[0]
    conn.close()
    return role == "COORDINATOR"


#Verifying if event creator is a coordinator 
def verify_role(UserID):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Role, ApprovalStatus FROM Users WHERE UserID=?", (UserID,)) #checks role of user from Users table
    row = cursor.fetchone() #returns first row of database
    role = row[0]
    approval_status = row[1]
    if (role == "COORDINATOR" or role == "ADMIN") and approval_status == "approved":
        print("Role Approved")
        return True
    else:
        print("Role Denied")
        return False
    


# Function to create a new event in the database
def create_event(club_id, title, description, date_, time_, venue_id, user_id):
    # Validate title and description
    if not title.isalpha() or not description.isalpha():
        return "Title and description should contain only alphabetic characters."

    try:
        conn = sqlite3.connect('MiniEpic.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Events (Club_id, Title, Description, Date_, Time_, Venue_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (club_id, title, description, date_, time_, venue_id))
        conn.commit()

        print("Event Created")
        return "Event Created Successfully!"
    except sqlite3.IntegrityError as e:
        error_message = str(e)
        if "UNIQUE constraint failed: Events.Title" in error_message:
            return "Title already exists. Please choose a different title."
        elif "UNIQUE constraint failed: Events.Description" in error_message:
            return "Description already exists. Please choose a different description."
        else:
            return "An error occurred while creating the event."

    finally:
        conn.close()

# Function to register a user for a specific event
def register_for_event(event_id, user_id):
    error_message = None  # Initialize error message variable
    
    try:
        conn = sqlite3.connect('MiniEpic.db')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO EventRegistration (EventID, UserID) VALUES (?, ?)", (event_id, user_id))
        conn.commit()
        
        cursor.execute("SELECT ClubID FROM Events WHERE EventID=?", (event_id,))
        club = cursor.fetchone()
        
        cursor.execute("SELECT ApprovalStatus FROM ClubMemberships WHERE ClubID = ? AND UserID = ?", (str(club[0]), str(user_id)))
        approval = cursor.fetchone()
        
        if approval is not None:
            cursor.execute("UPDATE EventRegistration SET ApprovalStatus = 'approved' WHERE EventID = ? AND UserID = ?", (event_id, user_id))
            conn.commit()
        
    except sqlite3.IntegrityError:
        error_message = "Error: This user is already registered for this event."
    finally:
        conn.close()
    
    return error_message




#views             
    
def view_events(): 
    conn, cursor = connect_to_database()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    result = [list(row) for row in events]
    
    conn.close()
    return result
#changed above


# Function to retrieve details of events user is registered for
def fetch_user_event_registrations(userID): 
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EventRegistration WHERE UserID = ?", (userID,))
    rows = cursor.fetchall()
    registered_events = [list(row) for row in rows]
    conn.close()
    return registered_events




# Function to retrieve events coordinated by a specific user
def coordinator_view_events(UserID): 
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Events.* FROM ViewClubCoordinators JOIN Events on ViewClubCoordinators.ClubID = Events.ClubID WHERE ViewClubCoordinators.UserID = ?", (UserID,))
    events = cursor.fetchall()
    result = [list(row) for row in events]
    conn.close()
    return result

# Function to retrieve events coordinated by a specific user with pending approvals
def coordinator_view_events_pending(UserID):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Events.* FROM ViewClubCoordinators JOIN Events on ViewClubCoordinators.ClubID = Events.ClubID WHERE ViewClubCoordinators.UserID = ?", (UserID,))
    events = cursor.fetchall()
    result = [list(row) for row in events]
    conn.close()
    return result

def coordinator_view_event_registrations(UserID):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT EventRegistration.* FROM ViewClubCoordinators JOIN Events ON ViewClubCoordinators.ClubID = Events.ClubID JOIN EventRegistration ON Events.EventID = EventRegistration.EventID WHERE ViewClubCoordinators.UserID = ? AND EventRegistration.ApprovalStatus = ?", (UserID, "approved"))
    registrations = cursor.fetchall()
    result = [list(row) for row in registrations]
    conn.close()
    return result


def coordinator_view_pending_event_registrations(UserID):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    # Use a tuple for parameter substitution
    cursor.execute("SELECT ClubID FROM Clubs WHERE CoordinatorID = ?", (UserID,))
    coordinatorClub = cursor.fetchone()

    cursor.execute("SELECT ER.RegistrationID, E.Title, U.Name || ' ' || U.Surname, ER.ApprovalStatus FROM EventRegistration ER, Events E, Users U WHERE ER.EVentID = E.EVentID AND ER.ApprovalStatus = 'pending' AND ER.UserID = U.UserID AND E.ClubID = ?", (coordinatorClub[0],))
    registrations = cursor.fetchall()
    result = [list(row) for row in registrations]
    conn.close()
    return result


# Function to retrieve all events for admin view
def admin_view_events(): 
    conn, cursor = connect_to_database()
    cursor.execute("SELECT * FROM View_Events")
    events = cursor.fetchall()
    result = [list(row) for row in events]
    
    conn.close()
    return result

# Function to retrieve events with pending approvals for admin view
def admin_view_events_pending():
    conn, cursor = connect_to_database()
    cursor.execute("SELECT * FROM View_Events WHERE ApprovalStatus = 'pending'")
    events = cursor.fetchall()
    result = [list(row) for row in events]
    
    conn.close()
    return result

# Function to verify if a user is registered for a specific event
def accept_event_registration(user_id, event_id): 
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EventRegistration WHERE UserID = ? AND EventID = ?", (user_id, event_id))
    row = cursor.fetchone()

    if row:
        cursor.execute("UPDATE EventRegistration SET ApprovalStatus = 'approved' WHERE UserID = ? AND EventID = ?", (user_id, event_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
    
def reject_event_registration(user_id, event_id):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EventRegistration WHERE UserID = ? AND EventID = ?", (user_id, event_id))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM EventRegistration WHERE UserID = ? AND EventID = ?", (user_id, event_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

#updates     #######################################
    
    # Function to update details of an existing event
def update_event(event_id, title=None, description=None, date_=None, time_=None, venue_id=None):
    conn, cursor = connect_to_database()
    update_query = "UPDATE Events SET"
    if title:
        update_query += " Title=?,"
    if description:
        update_query += " Description=?,"
    if date_:
        update_query += " Date_=?,"
    if time_:
        update_query += " Time_=?,"
    if venue_id:
        update_query += " Venue_id=?,"
    # Remove the last comma
    update_query = update_query[:-1]
    update_query += " WHERE Event_id=?"
    update_values = []
    if title:
        update_values.append(title)
    if description:
        update_values.append(description)
    if date_:
        update_values.append(date_)
    if time_:
        update_values.append(time_)
    if venue_id:
        update_values.append(venue_id)
    update_values.append(event_id)
    cursor.execute(update_query, tuple(update_values))
    conn.commit()
    conn.close()

    # Function to cancel a user's registration for an event
def cancel_event_registration(registration_id):
    conn, cursor = connect_to_database()
    cursor.execute("DELETE FROM Event_Registration WHERE Registration_id=?", (registration_id,))
    conn.commit()
    conn.close()

# Function to approve a user's registration for an event
def approve_registration(registration_id):
    conn, cursor = connect_to_database()
    cursor.execute("UPDATE Event_Registration SET ApprovalStatus='approved' WHERE Registration_id=?", (registration_id,))
    conn.commit()
    conn.close()

# Function to reject a user's registration for an event
def reject_registration(registration_id):#ONCE A REGISRTRATION IS REJECTED, IT SHOULD BE DELETED SO USE THE CANCEL_EVENT_REGISTRATION FUNCTION INTO THIS
    conn, cursor = connect_to_database()
    cursor.execute("UPDATE Event_Registration SET ApprovalStatus='rejected' WHERE Registration_id=?", (registration_id,))
    cancel_event_registration(registration_id)
    conn.commit()
    conn.close()

# Function to add a new venue to the database
def create_venue(venue_name):
    conn, cursor = connect_to_database()
    cursor.execute("INSERT INTO Venues (Venue_name) VALUES (?)", (venue_name,))
    conn.commit()
    conn.close()

# Function to delete a venue from the database
def delete_venue(venue_id):
    conn, cursor = connect_to_database()
    cursor.execute("DELETE FROM Venues WHERE Venue_id=?", (venue_id,))
    conn.commit()
    conn.close()

# Function to update details of an existing venue
def update_venue(venue_id, venue_name):
    conn, cursor = connect_to_database()
    cursor.execute("UPDATE Venues SET Venue_name=? WHERE Venue_id=?", (venue_name, venue_id))
    conn.commit()
    conn.close()

#deletes ##############################################
# Function to delete an event from the database
def delete_event(event_id):
    conn, cursor = connect_to_database()
    cursor.execute("DELETE FROM Events WHERE Event_id=?", (event_id,))
    conn.commit()
    conn.close()

# Function to retrieve details of a specific event
def get_event_details(event_id): 
    conn, cursor = connect_to_database()
    cursor.execute("SELECT * FROM Events WHERE Event_id=?", (event_id,))
    event_details = cursor.fetchone()
    conn.close()
    return event_details

# Function to retrieve all events a user is registered for
def get_registered_events_for_user(user_id): 
    conn, cursor = connect_to_database()
    cursor.execute("SELECT * FROM View_Event_Registration WHERE User_id=?", (user_id,))
    registered_events = cursor.fetchall()
    conn.close()
    return registered_events

# Function to retrieve details of a specific venue
def get_venue_details(venue_id):
    conn, cursor = connect_to_database()
    cursor.execute("SELECT * FROM Venues WHERE Venue_id=?", (venue_id,))
    venue_details = cursor.fetchone()
    conn.close()
    return venue_details

# Function to retrieve all venues stored in the database
def get_all_venues():
    conn, cursor = connect_to_database()
    cursor.execute("SELECT VenueName FROM Venues")
    all_venues = [venue[0] for venue in cursor.fetchall()]
    conn.close()
    return all_venues


for row in coordinator_view_pending_event_registrations(2):
    print(row)