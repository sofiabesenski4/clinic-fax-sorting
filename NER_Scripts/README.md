README.md
Sofia Besenski
Feb 9 2018


The NERServer must be running on port 9000 in the background for the scripts to work,
so the main script which runs will start it before any of this is executed.



The command to run the test from the terminal in linux is:
	python3 Interact_With_NERServer.py | python3 Interpret_Annotations.py

the inputs are hardcoded into the Interact_With_NERServer script as test1.txt
which will output a list of the tags found in the input indicating a PERSON name was found

(Nested) Required Directory structure:

-app:

--NER: folder containing the scripts and everything we are running
-------test1.txt: file which is used as input, currently

--nerzip: place where the stanford-ner package was unzipped
-------stanford-ner-2017-06-09: folder containing the jar files containing classifiers
		
