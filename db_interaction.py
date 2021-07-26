#psycopg_testing.py
from psycopg2 import sql
import psycopg2
import datetime

#print(psycopg2.__version__)
#conn = psycopg2.connect("dbname = test_patients user=teb8")
#db_ptr = conn.cursor()
#results = db_ptr.execute("SELECT * FROM iclinic_data;")
#print("first: ",str(db_ptr.fetchone()))
#print("second: ", str(db_ptr.fetchone()))
#print("third: ", str(db_ptr.fetchone()))
#print(str(db_ptr.fetchall()))

#the following methods need to be satisfied:
#def insert_patient_tuples_into_db(db_ptr, patient_tuples):
"""
Input: database_name = name of postgresql database to connect to 
	   username = the username which we are attempting to connect to the postgresql database with 
Output:conn_ptr = connection pointer to the postgresql database. A transactional database cursor must be instantiated before anything
					can be done with the specific table, but by separating these pointers, each transaction will be recorded in a long
					session
"""

def make_connection_to_db(database_name,username):
	try:
		conn_ptr = psycopg2.connect("dbname={} user={}".format(database_name,username))
		return conn_ptr
	except:
		print("error encountered when trying to connect to the database{} with username{}".format(database_name,username))
		
	

"""
Input: conn_ptr = psycopg2 connection object to the database we are dealing with
	   patient_tuple = patient to be inserted into the database, taking the form (string PHN, string first_name, string last_name, datetime_object DOB)
"""
def insert_patient_into_db(conn_ptr,patient_tuple,table_name):
	#using a with statement here makes this happen in one postgresql transaction, which is recorded
	with conn_ptr:
		with conn_ptr.cursor() as db_ptr:
			print(str(patient_tuple))
			db_ptr.execute( sql.SQL("Insert into {} values (%s,%s,%s,%s)").format(sql.Identifier(table_name)) , patient_tuple)
			db_ptr.close()

def select_all(conn_ptr, table_name):
	with conn_ptr:
		with conn_ptr.cursor() as db_ptr:
			db_ptr.execute(sql.SQL("Select * from {};").format(sql.Identifier(table_name)))
			for record in db_ptr:
				print(record)
			db_ptr.close()
#def PHN_vs_DOB_vs_partial_name_query(db_ptr, found_PHNs, found_datetime_objs, found_full_names)
def PHN_vs_DOB_vs_partial_name_query(connection_ptr, found_PHNs, found_datetime_objs, found_full_names, table_name):
	if len(found_PHNs) == 0 or len(found_datetime_objs) == 0 or len(found_full_names)==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_phns" in table:
					db_ptr.execute("drop table found_phns;")
				elif "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
				elif "found_partial_names" in table:
					db_ptr.execute("drop table found_partial_names;")
			try:
				db_ptr.execute("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
			except:
				
				print("error occured when trying to create found_phns table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
			except:
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
				print("error occured when trying to create found_partial_names table in  PHN_vs_DOB_vs_partial_name_query")
				return
			partial_name_list = []
			[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
			
			found_PHN_list = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
			#print(found_datetime_objs)
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			found_partial_name_list = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
			
			[db_ptr.execute("Insert into found_phns values (%s,%s)", element) for element in found_PHN_list]
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			[db_ptr.execute("Insert into found_partial_names values (%s,%s)", element) for element in found_partial_name_list]
			
			db_ptr.execute("""select * from fax_test_1, found_phns, found_dobs, found_partial_names 
								where fax_test_1.fax_line = '15737' and fax_test_1.phn=found_phns.phn and found_dobs.dob = fax_test_1.dob
								and (lower(found_partial_names.partial_name) = lower(fax_test_1.first_name) or lower(found_partial_names.partial_name)=lower(fax_test_1.last_name));""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_phns;")
			db_ptr.execute("DROP table found_dobs;")
			db_ptr.execute("DROP table found_partial_names;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
			
def PHN_vs_DOB_query(connection_ptr, found_PHNs, found_datetime_objs, table_name):
	if len(found_PHNs) == 0 or len(found_datetime_objs) ==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_phns" in table:
					db_ptr.execute("drop table found_phns;")
				elif "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
			try:
				db_ptr.execute("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
			except:
				
				print("error occured when trying to create found_phns table in  PHN_vs_DOB_vs_partial_name_query")
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
			
			found_PHN_list = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			
			[db_ptr.execute("Insert into found_phns values (%s,%s)", element) for element in found_PHN_list]
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			
			db_ptr.execute("""select * from fax_test_1, found_phns, found_dobs 
								where fax_test_1.fax_line = '15737' and fax_test_1.phn=found_phns.phn and found_dobs.dob = fax_test_1.dob;""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_phns;")
			db_ptr.execute("DROP table found_dobs;")
			
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
def PHN_vs_partial_name_query(connection_ptr, found_PHNs, found_full_names, table_name):
	if len(found_PHNs) == 0 or len(found_full_names)==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_phns" in table:
					db_ptr.execute("drop table found_phns;")
				elif "found_partial_names" in table:
					db_ptr.execute("drop table found_partial_names;")
			try:
				db_ptr.execute("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
			except:
				
				print("error occured when trying to create found_phns table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
			except:
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
				print("error occured when trying to create found_partial_names table in  PHN_vs_DOB_vs_partial_name_query")
				return
			partial_name_list = []
			[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
			
			found_PHN_list = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
			found_partial_name_list = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
			
			[db_ptr.execute("Insert into found_phns values (%s,%s)", element) for element in found_PHN_list]
			
			
			[db_ptr.execute("Insert into found_partial_names values (%s,%s)", element) for element in found_partial_name_list]
			
			db_ptr.execute("""select * from fax_test_1, found_phns, found_partial_names 
								where fax_test_1.fax_line = '15737' and fax_test_1.phn=found_phns.phn and
								 (lower(found_partial_names.partial_name) = lower(fax_test_1.first_name) or lower(found_partial_names.partial_name)=lower(fax_test_1.last_name));""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_phns;")
			
			db_ptr.execute("DROP table found_partial_names;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
def DOB_vs_partial_name_query(connection_ptr, found_datetime_objs, found_full_names, table_name):
	if len(found_datetime_objs) == 0 or len(found_full_names)==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
				elif "found_partial_names" in table:
					db_ptr.execute("drop table found_partial_names;")
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
			except:
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
				print("error occured when trying to create found_partial_names table in  PHN_vs_DOB_vs_partial_name_query")
				return
			partial_name_list = []
			[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
			
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			found_partial_name_list = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
			
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			[db_ptr.execute("Insert into found_partial_names values (%s,%s)", element) for element in found_partial_name_list]
			
			db_ptr.execute("""select * from fax_test_1, found_dobs, found_partial_names 
								where   fax_test_1.fax_line = '15737' and found_dobs.dob = fax_test_1.dob
								and (lower(found_partial_names.partial_name) = lower(fax_test_1.first_name) or lower(found_partial_names.partial_name)=lower(fax_test_1.last_name));""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_dobs;")
			db_ptr.execute("DROP table found_partial_names;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
def DOB_query(connection_ptr, found_datetime_objs, table_name):
	if len(found_datetime_objs) == 0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
				return
			
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			
			db_ptr.execute("""select * from fax_test_1, found_dobs 
								where   fax_test_1.fax_line = '15737' and found_dobs.dob = fax_test_1.dob
								;""") 
			ret_list = db_ptr.fetchall()
			print("RET_LIST: " +str(ret_list))
			db_ptr.execute("DROP table found_dobs;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list


def main():
	connection_ptr = make_connection_to_db("test_patients", "thomas")
	#insert_patient_into_db(connection_ptr, ("1234569894","Psycooo","PGGG",datetime.date(year = 2018, month = 5, day = 18)), "iclinic_data")
	select_all(connection_ptr, "fax_test_1")
	test_found_phns = ["1234567894","1234567890","1234567896"]
	test_found_DOBs = [datetime.date(year = 1994, day = 4, month = 10)]
	test_found_part_names = ["Bez Thomas", "Melvin"]
	print("PHN_vs_DOB_vs_partial_name_query", PHN_vs_DOB_vs_partial_name_query(connection_ptr, test_found_phns,test_found_DOBs, test_found_part_names, "fax_test_1"))
	print("PHN_vs_DOB_query", PHN_vs_DOB_query(connection_ptr, test_found_phns,test_found_DOBs,"fax_test_1"))
	print("PHN_vs_partial_name_query", PHN_vs_partial_name_query(connection_ptr, test_found_phns,test_found_part_names,"fax_test_1"))
	print("DOB_vs_partial_name_query", DOB_vs_partial_name_query(connection_ptr, test_found_DOBs,test_found_part_names,"fax_test_1"))



	connection_ptr.close()


if __name__ == "__main__":
	main()


"""
this query allows for 1 character of variability at the beginning of the name "Parker"
Idea:
use this idea to create a pattern for each name and PHN found in the document, with a wildcard inserted at postion in the string  
select * from patients where patients.last_name ~* '[abcdefghijklmnopqrstuvwxyz]arker' and CHAR_LENGTH(patients.last_name)=6;

"""
