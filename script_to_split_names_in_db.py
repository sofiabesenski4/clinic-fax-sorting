#script_to_split_names_in_db.py

from pg import DB

"""
modelling it after:
select * from split_part((select first_name from iclinic_data where phn='1234567890'),'ho',1);



This will return all entries where there is multiple strings in the first_name column
select * from iclinic_data where (first_name like '% %');





JUST RUN THIS SQL COMMAND IN PSQL FOR THE DATABASE AND WE ARE SET
update iclinic_data 
	set first_name = split_part(first_name, ' ', 1)
	where (first_name like '% %'); 



"""

