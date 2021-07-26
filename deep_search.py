#deep_search.py
#This module contains the methods required for the pipeline to perform deeper search operations
"""
IDEA: 
Given either a datetime object representing a DOB or a string containing digits (PHN),
find all database matches which correspond to the given input


Process(input) 
if input is a PHN
patient_names = check db for patients with that phn and return first and last name

if input is DOB
patient_names = check db for patients with that DOB and return furst and last name

PSEUDOCODE:
	search_dob(datetime DOB):
		
	
	
	search_phn(string PHN):
	
	


"""
import argparse
import re
import datetime
from psycopg2 import sql
import psycopg2
#THIS IS THE MAIN FUNCTION AT WORK IN THE MODULE
"""
INPUT:
clue: either a DOB or PHN which we want to investigate in the text,
text: the text body which we are trying to find out the patient subject of
database_name: the database name to query
table_name: the name of the relation which we are going to look for entries within
username: the name of the current user and user which is accessing the database relation
"""
def deep_search(clue, text, database_name, table_name, username):
	#patient_dict is a dictionary that will map each pattern back to the clue/patient where it originated from
	patient_dict = {}
	#first verify that all inputs are not None
	if not clue or not text or not database_name or not table_name or not username:
		print("Nonetype detected in input parameters of deep_search from the module deep_search")
		return
	#check the type of the input:
	conn_ptr = psycopg2.connect("dbname={} user={}".format(database_name,username))
	
	if type(clue) == type(datetime.date.today()):
		print("clue type is datetime obj")
		#get the patient names and PHN's with that DOB
		return dob_search(clue,text,conn_ptr,table_name,username)
	elif type(clue) == type("123"):
		print("clue type is  PHN")
		#get the patient names with that PHN
		return phn_search(clue, text, conn_ptr, table_name, username)
	else:
		
		print("clue type is incompatible with input specs")
		return


def phn_search(clue, text, conn_ptr, table_name, username):
	orginal_names = PHN_query(clue, conn_ptr, table_name)
	return None

"""PSEUDO: input DOB
A = list of patient names corresponding to a given DOB in the database
B= list of patient PHNs corresponding to a given DOB in the db


Search for unaltered names


Search for 1 char off names


"""
def dob_search(clue, text, conn_ptr, table_name, username):
	results = DOB_query(clue,conn_ptr,table_name)
	original_names = results[0]
	original_phns = results[1]
	print("Database Names:" + str(original_names))
	print("Database PHNs:" + str(original_phns))
	#now must scan through text for these names and PHNs
	print("searching the text for these names and PHN w no wildcards")
	
	names_found_match_objs = scan_for_patterns(original_names,text)
	phns_found_match_objs = scan_for_patterns(original_phns,text)
	names_found = [element.group(0) for element in names_found_match_objs if element]
	phns_found = [element.group(0) for element in phns_found_match_objs if element]
	[print("name found: " + str(element)) for element in names_found if element]
	[print("phn found: " + str(element)) for element in phns_found if element]
	
	if not names_found==None or not phns_found==None:
		return (names_found,phns_found)
	
	#now try to do the same thing with patterns including a wildcard at everys spot
	variance_1_name_patterns = generate_variance_patterns(original_names)
	variance_1_phn_patterns = generate_variance_patterns(original_phns)
	#now searching w the new patterns
	print("searching with 1 wildcard")
	names_found_var_1 = scan_for_patterns(variance_1_name_patterns,text)
	phns_found_var_1 = scan_for_patterns(variance_1_phn_patterns,text)
	names_found = [element.group(0) for element in names_found_var_1 if element]
	phns_found = [element.group(0) for element in phns_found_var_1 if element]
	
	[print("name found: " + str(element)) for element in names_found_var_1 if element]
	[print("phn found: " + str(element)) for element in phns_found_var_1 if element]

	if not names_found==None or not phns_found==None:
		return (names_found,phns_found)
	return None

def PHN_query(target_phn, conn_ptr, table_name):
	names = []
	with conn_ptr.cursor() as curs:
		sql_tuple = (target_phn,)
		curs.execute(sql.SQL("SELECT first_name, last_name from {} where phn=%s;").format(sql.Identifier(table_name)), sql_tuple)
		for value in curs:
			for name in value:
				print(name)
				names.append(name)
	
	return names
	
def DOB_query(target_DOB,conn_ptr, table_name):
	names=[]
	phns = []
	with conn_ptr.cursor() as curs:
		sql_tuple = (target_DOB,)
		curs.execute(sql.SQL("SELECT first_name, last_name, phn from {} where dob=%s;").format(sql.Identifier(table_name)), sql_tuple)
		for value in curs:
			names.append(value[0].strip())
			names.append(value[1].strip())
			phns.append(value[2].strip())
		
	
	return (names,phns)


def generate_variance_patterns(target_list):
	return_patterns = []
	for target in target_list:
		if not target:
			continue
		for index, char in enumerate(target):
			#print (str(index)+ " "+char)
			new_string = target[0:index] + "." + target[index+1:]
			return_patterns.append(new_string)
	print(str(return_patterns))
	return return_patterns

#returns matches object
def scan_for_patterns(strings,text):
	matches = []
	for string in strings:
		matches.append(re.search(string,text))
	return matches

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("--db","--database",required =True)
	ap.add_argument("--t","--tablename", required = False)
	ap.add_argument("--u","--systemusername",required=True)
	test_dob=datetime.date(year=1994,month=10,day=4)
	args = ap.parse_args()
	text = "Robbi smith blahblahblah 124"
	
	"""
	deep_search('123', text, args.db , args.t, args.u)
	print("searching via DOB")
	print(str(datetime.date(year=1994,month=10,day=4)))
	deep_search(test_dob, text, args.db , args.t, args.u)
	"""

if __name__ == "__main__":
	main()
