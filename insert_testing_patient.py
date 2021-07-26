#insert_testing_patient.py
import datetime
from pg import DB
"""
Feb 27 2018
This script should be run to enter some patients into the table called 'patients' in the database called 'patient_db_test'


DATE formats:
YMD - year-month-day is the most desirable format, considered ISO 8601 standards
"""

db = DB("test_patients")
db.insert('patients', first_name = "NICHOLAS ANDREW", last_name = "MARSDEN", phn = "9067 062 924", dob = datetime.date(1946, 10, 6))
db.insert('patients', first_name = "JOHNNY ALAN GEORGE", last_name = "LUCK", phn = "9136 527 693", dob = datetime.date(1941, 5, 12))
db.insert('patients', first_name = "ELIZABETH M", last_name = "CARLEY", phn = "9051 748 373", dob = datetime.date(1939, 3, 25))
