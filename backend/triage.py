import json
import sys


def loadJSON():
    try:
        db_fp = open("illness.json")
    except:
        try:
            db_fp = open("illness_bak.json")
        except:
            return None
    db = json.load(db_fp)
    db_fp.close()
    return db


def assessPatient(db, symptom):
    """
    Given database and symptom
    returns illness linked to symptom
    """
    for entry in db:
        if symptom in entry.keys():
            return entry[symptom]
        
    return "Need more info for diagnosis"


db = loadJSON()
if db == None:
    print("Error: database unreachable")
    sys.exit()

symptom = input("Enter symptom: ").lower()
diagnosis = assessPatient(db, symptom)

print(diagnosis)