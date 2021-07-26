#res	ult_analysis.py
"""
idea:
so we want to look through a file directory called Test_Results, and find out how many of what type of matches have been made
from the processed samples

-start a tally for each type of match
-navigate to folder
-for every file in directory:
	-parse through to find if a match!= F
		-record the sample number and match in the csv
		-
"""

import os
import csv
import re
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("--folder","--f",required=True)
args = ap.parse_args()

def get_txt_paths(directory_name, pdf_paths = []):
	#print(str(os.listdir(directory_name)))

	for file_name in os.listdir(directory_name):
		if file_name.endswith(".txt"):
			pdf_paths.append(os.path.join(directory_name, file_name))	
		elif os.path.isdir(os.path.join(directory_name, file_name)):
			#print("directory: " + file_name)
			pdf_paths =get_pdf_paths(os.path.join(directory_name,file_name),pdf_paths)
	return pdf_paths


txt_paths = get_txt_paths(str(args.folder))
capture = re.compile(r"'(.*?)'")
results=[]
#print(str(txt_paths))
for txt_doc in txt_paths:
	fp = open(txt_doc, "r")
	doc_results=[str(txt_doc)]
	
	for line in fp:
		
		if line.startswith("Patient Hypothesis:"):
			 doc_results.append(str(capture.search(line).group(1)))
			 #print("here:" +str(capture.search(line).group(1)))
	#print( str(doc_results))
	results.append(doc_results)
results_dict={"A":0, "B":0, "C":0,"D":0,"F":0,"Multiple A Matches":0,"Multiple B Matches":0,"Multiple C Matches":0,"Multiple D Matches":0}
errors=0
for result in results:
	try:

		results_dict[str(result[-1])]+=1
	except:
		errors+=1
		continue
print(str(results_dict.items()))

fp=open("Nov7-1_analysis_of_{}.txt".format(args.folder),"w")
fp.write("""Results Dictionary:
A matches: {}
B matches: {}
C matches: {}
D matches: {}
F matches: {}
Multiple A Matches: {}
Multiple B Matches: {}
Multiple C Matches: {}
Multiple D Matches: {}
errors : {}
""".format(results_dict["A"],results_dict["B"],results_dict["C"],results_dict["D"],results_dict["F"],results_dict["Multiple A Matches"],results_dict["Multiple B Matches"],results_dict["Multiple C Matches"],results_dict["Multiple D Matches"], str(errors)))


