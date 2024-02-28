import sqlite3
import Login

def CreateUsersTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
        #connection to database
    
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Surname TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Role TEXT DEFAULT 'STUDENT' NOT NULL CHECK(Role IN ('ADMIN', 'COORDINATOR', 'STUDENT')),
            ApprovalStatus TEXT DEFAULT 'pending' NOT NULL CHECK(ApprovalStatus IN ('approved', 'pending', 'rejected')),
            CreatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ); ''')
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS users_insert_trigger
            AFTER INSERT ON Users
            FOR EACH ROW
            BEGIN
                UPDATE Users SET CreatedTimestamp = NEW.CreatedTimestamp WHERE UserID = NEW.UserID;
            END; ''')

            cursor.execute('''CREATE TRIGGER IF NOT EXISTS users_update_trigger
            AFTER UPDATE ON Users
            FOR EACH ROW
            BEGIN
                UPDATE Users SET UpdatedTimestamp = CURRENT_TIMESTAMP WHERE UserID = NEW.UserID;
            END; ''')

        
            conn.commit()
    except Exception as e:
        print(e)

    finally:
        conn.close()

def CreateClubsTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
        #connection to database
    
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Clubs (
            ClubID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            CoordinatorID INTEGER NOT NULL UNIQUE,
            Description TEXT,
            ValidityStatus TEXT DEFAULT 'pending' NOT NULL CHECK(ValidityStatus IN ('approved', 'pending', 'rejected')),
            CreatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (CoordinatorID) REFERENCES Users(UserID)
            );''')
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS clubs_insert_trigger
            AFTER INSERT ON Clubs
            FOR EACH ROW
            BEGIN
                UPDATE Clubs SET CreatedTimestamp = NEW.CreatedTimestamp WHERE ClubID = NEW.ClubID;
            END; ''')
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS clubs_update_trigger
            AFTER UPDATE ON Clubs
            FOR EACH ROW
            BEGIN
                UPDATE Clubs SET UpdatedTimestamp = CURRENT_TIMESTAMP WHERE ClubID = NEW.ClubID;
            END; ''')
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateLoginTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
        #connection to database
    
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Login(
            UserID INTEGER PRIMARY KEY,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            CreatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
            ) ''')    
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS login_insert_trigger
            AFTER INSERT ON Login
            FOR EACH ROW
            BEGIN
                UPDATE Login SET CreatedTimestamp = NEW.CreatedTimestamp WHERE UserID = NEW.UserID;
            END; ''')
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS login_update_trigger
            AFTER UPDATE ON Login
            FOR EACH ROW
            BEGIN
                UPDATE Login SET UpdatedTimestamp = CURRENT_TIMESTAMP WHERE UserID = NEW.UserID;
            END; ''')
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreatePhoneNumbersTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
        #connection to database
    
            cursor = conn.cursor() 
            cursor.execute('''CREATE TABLE IF NOT EXISTS PhoneNumber (
            UserID INTEGER PRIMARY KEY,
            PhoneNumber TEXT NOT NULL UNIQUE,
            CreatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
            ); ''')
            conn.commit()
            cursor.execute(''' CREATE TRIGGER IF NOT EXISTS phonenumber_insert_trigger
            AFTER INSERT ON PhoneNumber
            FOR EACH ROW
            BEGIN
                UPDATE PhoneNumber SET CreatedTimestamp = NEW.CreatedTimestamp WHERE UserID = NEW.UserID;
            END;''')
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS phonenumber_update_trigger
            AFTER UPDATE ON PhoneNumber
            FOR EACH ROW
            BEGIN
                UPDATE PhoneNumber SET UpdatedTimestamp = CURRENT_TIMESTAMP WHERE UserID = NEW.UserID;
            END; ''')
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateMembershipsTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
        #connection to database
    
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS ClubMemberships (
            MembershipID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            ClubID INTEGER NOT NULL,
            ApprovalStatus TEXT DEFAULT 'pending' NOT NULL CHECK(ApprovalStatus IN ('approved', 'pending', 'rejected')),
            CreatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
            CONSTRAINT UniqueUserClubID UNIQUE (UserID, ClubID)
        );;''')
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS clubmemberships_insert_trigger
            AFTER INSERT ON ClubMemberships
            FOR EACH ROW
            BEGIN
                UPDATE ClubMemberships SET CreatedTimestamp = NEW.CreatedTimestamp WHERE MembershipID = NEW.MembershipID;
            END; ''')
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS clubmemberships_update_trigger
            AFTER UPDATE ON ClubMemberships
            FOR EACH ROW
            BEGIN
                UPDATE ClubMemberships SET UpdatedTimestamp = CURRENT_TIMESTAMP WHERE MembershipID = NEW.MembershipID;
            END; ''')
            cursor.execute('''CREATE TRIGGER MaxClubsPerUser
            BEFORE INSERT ON ClubMemberships
            FOR EACH ROW
            WHEN (
                SELECT COUNT(*)
                FROM ClubMemberships
                WHERE UserID = NEW.UserID
            ) >= 3
            BEGIN
                SELECT RAISE(ABORT, 'Maximum number of clubs joined reached');
            END;''')
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateEventsTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn: 
        #connection to database
    
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Events (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClubID INTEGER,
            Title VARCHAR(20) NOT NULL,
            Description VARCHAR(30),
            Date_ DATE NOT NULL,
            Time_ TIME NOT NULL,
            Venue_id INTEGER NOT NULL,
            created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Venue_id) REFERENCES Venues(Venue_id),
            FOREIGN KEY (Club_id) REFERENCES Clubs(ClubID),
            CONSTRAINT UniqueDateTimeVenue UNIQUE (Date_, Time_, Venue_id)
            ); ''')
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS insert_timestamp_trigger
            AFTER INSERT ON Events
            FOR EACH ROW
            BEGIN
                UPDATE Events SET created_timestamp = IFNULL(NEW.created_timestamp, CURRENT_TIMESTAMP) WHERE Event_id = NEW.Event_id;
            END; ''')
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_timestamp_trigger
            BEFORE UPDATE ON Events
            FOR EACH ROW
            BEGIN
                UPDATE Events SET updated_timestamp = CURRENT_TIMESTAMP WHERE Event_id = NEW.Event_id;
            END; ''')
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateEventRegistrationTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS EventRegistration (
            RegistrationID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventID INTEGER NOT NULL,
            UserID INTEGER NOT NULL,
            ApprovalStatus TEXT DEFAULT 'pending' NOT NULL CHECK(ApprovalStatus IN ('approved', 'pending', 'rejected')),
            created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Event_id) REFERENCES Events(Event_id),
            FOREIGN KEY (User_id) REFERENCES Users(UserID)
            CONSTRAINT UniqueEventUserID UNIQUE (Event_id, User_id)
            );''')
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS insert_timestamp_trigger
            AFTER INSERT ON Event_Registration
            FOR EACH ROW
            BEGIN
                UPDATE Event_Registration SET created_timestamp = IFNULL(NEW.created_timestamp, CURRENT_TIMESTAMP) WHERE Registration_id = NEW.Registration_id;
            END; ''')
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_timestamp_trigger
            BEFORE UPDATE ON Event_Registration
            FOR EACH ROW
            BEGIN
                UPDATE Event_Registration SET updated_timestamp = CURRENT_TIMESTAMP WHERE Registration_id = NEW.Registration_id;
            END;''')
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateVenuesTable():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Venues(
	            VenueID INTEGER PRIMARY KEY AUTOINCREMENT,
	            VenueName VARCHAR(20) NOT NULL UNIQUE,
	            created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	            updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );''') 
            conn.commit()
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS insert_timestamp_trigger
            AFTER INSERT ON Venues
            FOR EACH ROW
            BEGIN
                UPDATE Venues SET created_timestamp = IFNULL(NEW.created_timestamp, CURRENT_TIMESTAMP) WHERE Venue_id = NEW.Venue_id;
            END;''') 
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_timestamp_trigger
            BEFORE UPDATE ON Venues
            FOR EACH ROW
            BEGIN
                UPDATE Venues SET updated_timestamp = CURRENT_TIMESTAMP WHERE Venue_id = NEW.Venue_id;
            END; ''') 
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateViews():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn:
            cursor = conn.cursor() 
            
            cursor.execute(''' CREATE VIEW IF NOT EXISTS AdminAccountView AS
            SELECT U.UserID, U.Name || ' ' || U.Surname AS 'Name', L.Username, U.Email, P.PhoneNumber, U.Role, U.ApprovalStatus, U.CreatedTimestamp, U.UpdatedTimestamp 
            FROM Users U, Login L, PhoneNumber P
            WHERE U.UserID = L.UserID AND U.UserID = P.UserID
            ORDER BY U.ApprovalStatus DESC, U.Name, U.Surname ''') 
            
            cursor.execute('''CREATE VIEW IF NOT EXISTS AdminAccountViewPending AS
            SELECT U.UserID, U.Name || ' ' || U.Surname AS 'Name', L.Username, U.Email, P.PhoneNumber, U.Role, U.ApprovalStatus, U.CreatedTimestamp, U.UpdatedTimestamp 
            FROM Users U, Login L, PhoneNumber P
            WHERE U.UserID = L.UserID AND U.UserID = P.UserID AND U.ApprovalStatus = 'pending'
            ORDER BY U.ApprovalStatus DESC, U.Name, U.Surname ''') 

            cursor.execute('''CREATE VIEW IF NOT EXISTS ClubsView AS
            SELECT C.ClubID, C.Name, U.Name || " " || U.Surname AS 'Coordinator Name', C.Description, C.CreatedTimestamp, C.UpdatedTimestamp
            FROM Clubs C, Users U
            WHERE C.ValidityStatus = 'approved' AND C.CoordinatorID = U.UserID;  ''') 
            
            cursor.execute('''CREATE VIEW IF NOT EXISTS AdminClubsView AS
            SELECT C.ClubID, C.Name, U.Name || " " || U.Surname AS 'Coordinator Name', C.Description, C.ValidityStatus, C.CreatedTimestamp, C.UpdatedTimestamp
            FROM Clubs C, Users U
            WHERE C.CoordinatorID = U.UserID; ''')
            
            cursor.execute('''CREATE VIEW IF NOT EXISTS AdminClubMembershipView AS
            SELECT M.MembershipID, U.Name || " " || U.Surname AS 'User Name', C.Name AS 'Club Name', M.ApprovalStatus, M.CreatedTimestamp, M.UpdatedTimestamp
            FROM Clubs C, Users U, ClubMemberships M
            WHERE M.UserID = U.UserID AND M.ClubID = C.ClubID
            ORDER BY M.CreatedTimestamp DESC;  ''') 
            
            cursor.execute(''' CREATE VIEW IF NOT EXISTS ViewClubMemberships AS
            SELECT M.MembershipID, C.Name, C.Description, U.UserID, U.Name || ' ' || U.Surname AS 'User Name', M.ApprovalStatus, M.CreatedTimestamp, M.UpdatedTimestamp 
            FROM Clubs C, Users U, ClubMemberships M 
            WHERE M.UserID = U.UserID AND M.ClubID = C.ClubID  
            ORDER BY M.CreatedTimestamp DESC ''') 
            
            cursor.execute('''CREATE VIEW IF NOT EXISTS ViewClubCoordinators AS
            SELECT U.UserID, U.Name || " " || U.Surname, C.Name, C.ClubID, (SELECT COUNT(*) FROM ClubMemberships M WHERE M.ClubID = C.ClubID AND M.ApprovalStatus = 'approved') AS 'Club members', C.ValidityStatus, C.CreatedTimestamp, C.UpdatedTimestamp
            FROM Users U, Clubs C
            WHERE U.UserID = C.CoordinatorID AND U.Role = 'COORDINATOR'
            ORDER BY U.Name, C.CreatedTimestamp DESC  ''')
            
            cursor.execute('''CREATE VIEW View_Events AS
            SELECT EVENTS.Title, EVENTS.Description, EVENTS.Date_, EVENTS.Time_, EVENTS.created_timestamp, EVENTS.updated_timestamp, Venues.VenueName
            FROM Events
            INNER JOIN Venues ON Events.VenueID = Venues.VenueID ''')  
    except Exception as e:
        print(e)
    finally:
        conn.close()  
def CreateAdmin():
    try: 
        with sqlite3.connect('MiniEpic.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Users WHERE UserID = 1 ''')
            row = cursor.fetchone()
            if row is None: 
                Login.create_account("dawijak", "ISE123", "Dawid", "Jakubowski", "dawijak@gmail.com", "0874384024")
                Login.promote_user(1)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def CreateDatabase():
    CreateUsersTable()
    CreateClubsTable()
    CreateLoginTable()
    CreatePhoneNumbersTable()
    CreateMembershipsTable()
    CreateEventsTable()
    CreateEventRegistrationTable()
    CreateVenuesTable()
    CreateViews()
    CreateAdmin()
