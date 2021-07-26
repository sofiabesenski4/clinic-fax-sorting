#insert_demo_data.py
"""

Target name: Chris Lane
date of birth: '1948', 9, '21' = 21 Sept 1948
PHN : 250-595-1551

Test_Results/1.txt: showing the functionality of partial name vs DOB match:
Target patient name: Janel L. Morris
Patient DOB: ('1967', 8, '18')
target PHN: 0987654321

Test_Results/2.txt: demonstrating DOB vs PHN matching
Target Patient name: Ricky Caterpillar
DOB:('1947', 10, '01')
PHN: 250-595-6793

Test_Results/3.txt: no possible matches here. The pdf is from a page of the Catcher in the Rye

Test_Results/4.txt: for this test case, I am going to demonstrate multiple matches in different categories:
This patient should match on all 4 different queries, and on ones considering partial name matches, twice
Target Patient Name 1: George Yakemchuk
DOB: ('2015', 4, '16')
PHN: 9201406376

This patient should match on all 4 different queries, and on ones considering partial name matches, three times, since 3 tokens in name
Target Patient Name 2: Yvonne D Moisson
DOB:  ('2015', 4, '16')
PHN: 844-716-7743

This patient, with the same DOB as the patient above, should also match, but only for the partial name vs DOB
Target Patient Name 3: Halzak Alison
DOB: (('2015', 4, '16'))
PHN: 1234567890
0
"""
from pg import DB
import datetime
import db_interaction
db_ptr = db_interaction.make_connection_to_db("test_patients")
"""
demo_patients = [("0987654321", "Janel","Morris", datetime.date(year = 1967,month =8,day = 18).isoformat()),("250-595-6793", "Ricky", "Caterpillar",
					datetime.date(year = 1947,month = 10,day =1).isoformat()),("9201406376","George","Yakemchuk",datetime.date(year = 2015,month =4,day =16).isoformat()),
					("844-716-7743","Yvonne","Moisson",datetime.date(year = 2015,month= 4,day = 16).isoformat() ),("1234567890","Alison","Halzak",datetime.date(year = 2015,month = 4,day = 16).isoformat())]
db_interaction.insert_patient_tuples_into_db(db_ptr,demo_patients)
"""
db_interaction.insert_patient_into_db(db_ptr,"Chris","Lane",datetime.date(1948,9,21).isoformat(),"250-595-1551")
					

