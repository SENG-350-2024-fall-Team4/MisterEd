import json

def loadJSON():
    # todo - don't hardcode to a single DB name
    db_fp = open("db.json")
    db = json.load(db_fp)
    db_fp.close()
    return db

def checkLogin(db, username, password):
    """
    Given database, username and password,
    returns True if password is correct, and False otherwise
    """
    for entry in db:
        if username not in entry.keys():
            continue
        elif entry[username] != password:
            return False
        else:
            return True
    return False

db = loadJSON()
print(db)  # For test purposes only

# Test code - makes sure DB can be properly queried
username = input("Enter a username: ")
password = input("Enter a password: ")

logIn = checkLogin(db, username, password)

if logIn == True:
    print("Logged in")
else:
    print("Incorrect login info")