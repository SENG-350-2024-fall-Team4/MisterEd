import json
import sys


def loadJSON():
    """
    Return illness database
    or backup of illness database
    """
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
    or ask for more information
    """
    for entry in db:
        for ill, sym in entry.items():
            if set(symptom).issubset(set(sym)):
                return ill
    return "Need more info for diagnosis"


db = loadJSON()
if db == None:
    print("Error: database unreachable")
    sys.exit()

symptomList = []
symptom = input("Enter symptom: ").lower()

while symptom != "":
    symptomList.append(symptom)
    symptom = input("Enter symptom: ").lower()

diagnosis = assessPatient(db, symptomList)

print("Diagnosis: " + diagnosis)