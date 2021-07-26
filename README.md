# MedicalLetterAI-CoreNLP
Implementation of MedicalLetterAI concepts using Stanford's pretrained models in CoreNLP and the Tesseract-OCR engine and pytesseract module.

Program execution:


NOTE:
To run the code, you must install unzip the stanford-ner-2017-06-09.zip into a file called nerzip in the root dir to run any code
in these files.

The main program can be executed by entering the main app folder, and running:
$python3 main.py --d <Path to PDF Directory from this folder>

Input directory may contain an arbitrary amount of pdf's with minimal preprocessing required.
The PDFs must be of relatively high quality, for the OCR engine to accurately recognize the words,
and the page mustn't be skewed or rotated in orientation.

Output is in the form of numbered text files, corresponding to the alphabetically ordered contents of the 
input directory folder.
Each txt file contains the encountered "person" names in the pdf document, in order of appearance,
followed by a "#####reached EOF or error occured#####" symbolizing the EOF.
A single line is generated after that line, specifying the hypothesized name of the patient discussed 
in the pdf medical letter. 
The hypothesis is based on a intuitive heuristic which assigns the patient name based on the the highest number of the following fields matching in the pdf:
  -Patient first or last name
  -Personal Health Number 
  -Date of Birth

The heuristic may not always be accurate, so there is room for improvement here.
