#Interact_with_Server.py
#Altered by Thomas Besenski, but the bulk of the code was taken from blog below
'''
This script utilizes the wrapper class "standfordcorenlp" which is an interface between a java server running the corenlp engine,
and the main program in this app.


A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server already running on port 9000 on local device.
Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/ 


'''

"""
NOTES:

So to use the functions in the following script, there must be a stanford corenlp server running on the port 9000, and this will communicate
with that server, returning the output of the annotations.

The following command will start the server, from inside the corenlp folder:

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,ner" -port 9000 -timeout 30000


NOTE: if you set -mx2g, the program will fail to communicate with the server. Possibly because there is not enough RAM to hold everything??


REQUIRES:
"""
from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import sys
import re
"""
Function: create_list_from_annotations:
input: annotation_list: a list of tuples of form ("word/token","annotation keyword")
	   desired_annotation: a string which represents the annotatiion which we filter for to build an output list
output: a list of elements which were annotated with the "desired_annotation" tag. 
		Elements adjacent to each other, with the same "desired_annotation" tag, are concatenated together to form one list element.
		

"""
def create_list_from_annotations(annotation_list, desired_annotation):
	#print(annotation_list)
	index = 0
	output_list = []
	
	while index  < (len(annotation_list)):
#		print(str(index))
		#this while will keep moving the index forward until we reach an element with the desired annotation
		while annotation_list[index][1] != desired_annotation and index<len(annotation_list)-1:
			index+=1
		#if will trigger if the current index points to a element with the desired annotation
		if annotation_list[index][1] == desired_annotation:
			output_entry = annotation_list[index][0]
			if index<len(annotation_list) -2 and desired_annotation == "PERSON" and annotation_list[index+1][0] == "," and annotation_list[index+2][1] == "PERSON":
				index+=1
				output_entry = output_entry + ","
			while index<len(annotation_list)-1 and annotation_list[index+1][1]==desired_annotation:
				index+=1
				output_entry = output_entry + " " + annotation_list[index][0]
			output_list.append(output_entry)
		index+=1
		#except:
		#	print("#####reached EOF or exception occurred#####")
		#	break"""

	return output_list	

	
#CODE TAKEN from  https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/


class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        #I reduced the number of properties the server needs to satisfy, reducing runtime
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens

"""
Function: init_corenlp()
Input: none
Ouptut: ptr to the corenlp interface

"""
def init_corenlp():
	sNLP = StanfordNLP()
	return sNLP
	
"""
Function: annotate_ner_with_corenlp(text,corenlp_ptr)
Input: text:str input which is the piece of writing/text to be annotated using the corenlp server interface
	   corenlp_ptr: pointer to the interface which is initialized using the init_corenlp function above
Output:
	output_lists: A python list with 3 elements; each element is a python list of tuples, each representing a list of 
					elements with their respective annotations.
					[Names_List, Dates_List, Numbers_List]
					Each of the lists has the format: Names_List = [(<name1>, "PERSON"), (<name2>,"PERSON"),...]
													  Dates_List = [(<date1>, "DATE"),(date2,"DATE"),....]
													  Numbers_List = [(<number1>, "NUMBER"),(<number2>,"NUMBER"),..]
"""
def annotate_ner_with_corenlp(text, corenlp_ptr):
	
	#print ("Annotate:", sNLP.annotate(text),'\n')
	#print ("POS:", sNLP.pos(text),'\n')
	#print ("Tokens:", sNLP.word_tokenize(text),'\n')
	#print("NER:" , corenlp_ptr.ner(text))
	#print(text)
	
	names_found = create_list_from_annotations(corenlp_ptr.ner(text),"PERSON")
	
	dates_found = create_list_from_annotations(corenlp_ptr.ner(text),"DATE")
	
	numbers_found = create_list_from_annotations(corenlp_ptr.ner(text),"NUMBER")
	#print ("Parse:", sNLP.parse(text),'\n')
	#print ("Dep Parse:", sNLP.dependency_parse(text),'\n')
	output_lists = [names_found,dates_found,numbers_found]
#	print("NAMES FOUND: ",names_found)
#	print("DATES FOUND: ",dates_found)
#	print("NUMBERS FOUND: ",numbers_found)
#	print(patient_hypothesis(names_found))
	return tuple(output_lists)
"""
Main function only used for testing the functions in this module
"""
if __name__ == "__main__":
	test_annotations= [("Patient","TEST"),("name","0"),("is","TEST"),("Besenski","PERSON"),(",","0"), ("Thomas","PERSON"),("B", "PERSON"),("END","0")]
	print(create_list_from_annotations(test_annotations, "PERSON"))
	print(create_list_from_annotations(test_annotations,"TEST"))
	
