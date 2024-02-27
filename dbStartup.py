import sqlite3

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
            cursor.execute('''CREATE TABLE Login(
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
            cursor.execute('''CREATE TABLE PhoneNumber (
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
       
