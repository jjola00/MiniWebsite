import sqlite3
######################################################################################################################################################################################
#Club Management
######################################################################################################################################################################################

################################################################################################################################################################################################################
#Inserts
#Verifying if club creator is a coordinator
def verify_role(UserID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT Role, ApprovalStatus FROM Users WHERE UserID=?", (UserID,)) #checks role of user from Users table
            row = cursor.fetchone() #returns first row of database
            role = row[0]
            approval_status = row[1]
            if (role == "COORDINATOR" or role == "ADMIN") and approval_status == "approved":
                return True
            else:
                return False
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

def verify_clubs_coordinated(UserID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Clubs WHERE CoordinatorID=?", (UserID,))
            row = cursor.fetchone()
            clubs_coordinated = row[0]
            return clubs_coordinated
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()
        
def get_ClubID(CoordinatorID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT ClubID FROM Clubs WHERE CoordinatorID=?",(CoordinatorID,))
            row = cursor.fetchone ()
            club_id = row[0]
            return club_id   
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()


#Creating a new club
def creating_club(Name, CoordinatorID, Description): 
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clubs Where Name=?", (Name,))
            row = cursor.fetchone()
            if row is None:
                cursor.execute("INSERT INTO Clubs (Name, CoordinatorID, Description) VALUES (?,?,?)", (Name, CoordinatorID, Description))
                conn.commit()
                return "Club Created, awaiting approval!"
            else:
                return "Club Creation Denied"
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

def get_club_id_using_sport_name(sport_name):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()

        cursor.execute("SELECT ClubID FROM Clubs WHERE Name = ?", (sport_name,))
        club_id = cursor.fetchone()

        if club_id:
            return club_id[0]
        else:
            print(f"No club found for sport name: {sport_name}")
            return None

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None

    finally:
        if conn:
            conn.close()
    
def get_club_id_for_user(UserID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()

            cursor.execute("SELECT ClubID FROM Clubs WHERE CoordinatorID = ?", (UserID,))
            club_id = cursor.fetchone()
            conn.close()
            if club_id is not None:
                return club_id[0]
            else:
                return None
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None
    finally:
        if conn:
            conn.close()
    
 

    
def verify_clubs_joined(UserID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ClubMemberships WHERE UserID=?", (UserID,))
            row = cursor.fetchone()
            clubs_joined = row[0]
            return clubs_joined
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()
    
def club_registration(UserID, ClubID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            if verify_clubs_joined(UserID) < 3:
                cursor.execute("SELECT * FROM Clubs WHERE ClubID=?", (ClubID,))
                row = cursor.fetchone()   

                if row is None:
                    raise ValueError("Club does not exist")
                else:
                    clubID = row[0]
                    cursor.execute("INSERT INTO ClubMemberships (UserID, ClubID) VALUES (?,?)", (UserID, clubID))
                    conn.commit()
                    print("Club Registration Successful")
            else:
                raise ValueError("Too many clubs joined")
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()


################################################################################################################################################################################################################
#Views
def user_view_clubs():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ClubsView")     
            rows = cursor.fetchall()
            result = [list(row) for row in rows]
    
            return result
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()


def user_views_memberships(userID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ViewClubMemberships WHERE ApprovalStatus = 'approved' AND UserID =?", (userID,))
            rows = cursor.fetchall()
            result = [list(row) for row in rows]
    
            return result
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

def coordinator_view_club_memberships(UserID):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ViewClubMemberships WHERE ApprovalStatus = 'approved' AND CoordinatorID = ?", (UserID,))
    rows = cursor.fetchall()
    club_members = [list(row) for row in rows]
    conn.close()
    return club_members

def coordinator_view_club_pending_memberships(UserID):
    conn = sqlite3.connect('MiniEpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT M.MembershipID, C.ClubID, U.Name || ' ' || U.Surname, M.ApprovalStatus FROM ClubMemberships M, Clubs C, Users U WHERE U.UserID = M.UserID AND C.ClubID = M.ClubID AND M.ApprovalStatus = 'pending' AND C.CoordinatorID = ?", (UserID,))
    rows = cursor.fetchall()
    club_members = [list(row) for row in rows]
    conn.close()
    return club_members

def update_membership_status(MembershipID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("UPDATE ClubMemberships SET ApprovalStatus='approved' WHERE MembershipID=?", (MembershipID,))
            conn.commit()
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

def reject_club_membership(MembershipID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ClubMemberships WHERE MembershipID=?", (MembershipID,))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()


def delete_club_membership(membership_id):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ClubMemberships WHERE MembershipID = ?", (membership_id,))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        if conn:
            conn.close()
    
def coordinator_club_view(CoordinatorID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLUBS")
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        if conn:
            conn.close()

def pending_clubs():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AdminClubsView WHERE ValidityStatus = 'pending'")
            rows = cursor.fetchall()
            result = [list(row) for row in rows]
            return result
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

    

def admin_view_clubs():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AdminClubsView")     
            rows = cursor.fetchall()
            result = [list(row) for row in rows]
    except sqlite3.Error as e:  
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()
    
    return result

def admin_view_clubs_pending():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AdminClubsView WHERE ValidityStatus = 'pending'")     
            rows = cursor.fetchall()
            result = [list(row) for row in rows]
            return result
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()
    

def admin_view_club_memberships():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AdminClubMembershipView")
            rows = cursor.fetchall()
            result = [list(row) for row in rows]
    
            return result
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

def verify_club_membership(UserID, ClubID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ClubMemberships WHERE UserID =? AND ClubID =?", (UserID, ClubID))
            row = cursor.fetchone()
            membership = row[0]
            if membership is not None:
                return True
            else:
                return False
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

################################################################################################################################################################################################################
#Update
def approve_club_membership(membershipID, CoordinatorID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ClubMemberships WHERE MembershipID = ?", (membershipID,))
            membership_row = cursor.fetchone()

            if membership_row is not None:
                cursor.execute("SELECT * FROM ClubMemberships M, Clubs C WHERE M.MembershipID = ? AND M.ApprovalStatus = 'pending' AND (C.ClubID = (SELECT ClubID FROM Clubs WHERE CoordinatorID = ?) OR ? = 1)", (membershipID, CoordinatorID, CoordinatorID))
                membership_row = cursor.fetchone()

                if membership_row is not None or CoordinatorID == 1:
                    cursor.execute("UPDATE ClubMemberships SET ApprovalStatus = 'approved' WHERE MembershipID = ?", (membershipID,))
                    conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

def approve_club(ClubID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clubs WHERE ClubID = ?", (ClubID,))
            club_row = cursor.fetchone()
            if club_row is not None:
                cursor.execute("UPDATE Clubs SET ValidityStatus = 'approved' WHERE ClubID = ?", (ClubID,))
                conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

def reject_club(ClubID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clubs WHERE ClubID = ?", (ClubID,))
            club_row = cursor.fetchone()
            if club_row is not None:
                cursor.execute("DELETE FROM Clubs WHERE ClubID =?", (ClubID,))
                conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()

################################################################################################################################################################################################################
#Deletes
        
def delete_club(ClubID):
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
            #connection to database
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ClubMemberships WHERE ClubID =?", (ClubID,))
            cursor.execute("DELETE FROM Events WHERE ClubID =?", (ClubID,))
            cursor.execute("DELETE FROM EventRegistration WHERE EventID = (SELECT EventID FROM Events WHERE ClubID = ?)", (ClubID,))
            cursor.execute("DELETE FROM Clubs WHERE ClubID =?", (ClubID,))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    finally:
        if conn:
            conn.close()
          

################################################################################################################################
    
#INSERTS
#Creating a new club
#ClubName = "Chess Club" 
#CoordinatorID = 31 #Data stored from login page
#Description = "Check mate"
#creating_club(ClubName, CoordinatorID, Description)

#Registering for a new club     
#Userid = 9 #Data stored from login page
#ClubName = "Baking Club"
#club_registration(Userid, ClubName)



#VIEWS
#Displays all approved clubs
#for record in user_view_clubs():
#   print(record)     

#Displaying all memberships of a specific user
#UserID = 8
#for record in user_views_memberships(UserID):
#    print(record)
        
#Displaying all memberships of a specific club
#CoordinatorID = 2
#for record in coordinator_view_club_memberships(CoordinatorID):
#    print(record)

#Display all pending memberships of a specific club
##CoordinatorID = 2
##for record in coordinator_view_club_pending_memberships(CoordinatorID):
   ## print(record)

#Displays all clubs including not approved
#for record in admin_view_clubs():
#    print(record)

#Displays only pending clubs
#for record in admin_view_clubs_pending():
#   print(record)
        
#Displays all memberships
#for record in admin_view_club_memberships():
#    print(record)
        




#UPDATES
#Approves club memberships
#MembershipID = 8
#CoordinatorID = 5
#approve_club_membership(MembershipID, CoordinatorID) 

#Approves clubs
#userID = 1 #Data from login
#clubID = 8
#approve_club(userID, clubID)

#Rejects clubs
#userID = 1 
#clubID = 6
#reject_club(userID, clubID) 
    



#DELETES
#Deletes clubs
#ClubID = 5
#delete_club(ClubID)
    
#Deletes memberships
#MembershipID = 2
#delete_membership(MembershipID)
