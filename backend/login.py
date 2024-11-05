import json

def loadJSON():
    # todo - don't hardcode to a single DB name
    db_fp = open("login.json")
    db = json.load(db_fp)
    db_fp.close()
    return db

def checkLogin(db, username, password):
    """
    Given database, username and password,
    returning a string based on login status (Admin, Medical, User, Fail)
    """
    for entry in db:
        if username not in entry.keys():
            continue
        elif entry[username] != password:
            return "Fail"
        else:
            return entry["Type"]
    return "Fail"

db = loadJSON()
print(db)  # For test purposes only

# Test code - makes sure DB can be properly queried
username = input("Enter a username: ")
password = input("Enter a password: ")

logIn = checkLogin(db, username, password)

if logIn != "Fail":
    print("Logged in as " + logIn)
else:
    print("Incorrect login info")