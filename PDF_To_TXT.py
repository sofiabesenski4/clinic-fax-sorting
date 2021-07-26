#Letter_To_Text.py
#Date Feb 1 2018
#most code is adapted from the example at https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

"""
Mar 6 2018:
Notes:
-altered the structure of the module such that it only contains a function to call.
This was done with the intention of importing the module into the main.py program,
instead of using operating system calls to run the script.
-This has resulted in a significant decrease in runtime.

"""
#using pytesseract as the ocr engine
import pytesseract
import argparse
##using opencv to feed image input into tesseract
import cv2
import PIL
import os
#PIL is the python imaging library, used by opencv
from PIL import *
#PIL uses numpy to represent images
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes

from PIL import Image
from PIL import ImageFilter
"""
convert_pdf_to_txt(pdf_path):
input: pdf_path = the path, relative to the pwd, to the pdf we want to perform OCR on.
output: 
"""
def convert_pdf_to_txt(pdf_path, degrees_of_rotation):
	images = convert_from_path(pdf_path, dpi = 300)
	#(amazingly) simply implementation(??)
	
	image_list =[]
	for i,image in enumerate(images):
		image.save(str(i) + ".jpg")
		#print(str(i)+".jpg")
		image_list.append(str(i)+".jpg")
		if i>4:
			break
	return ocr_images(image_list, degrees_of_rotation)


	
def ocr_images(image_list, degrees_rotation):
	output_strings = []
	#loading image and convert to grayscale
	for image_name in image_list:
		#print(image)
		#image = cv2.imread(image_name)
		#print(image.shape)
		#cv2.imshow("img,",image)
		#gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		gray = Image.open(os.path.join(os.getcwd(), image_name))
		#if degrees_rotation!= 0:
		#	gray = gray.rotate(degrees_rotation)
		gray = gray.point(lambda x: 0 if x<200 else 255)
		"""HERE IS WHERE WE CAN ADD IN OUR OWN FILTERS/PREPROCESSING EFFECTS TO INCREASE OCR ACCURACY DEPENDING ON DATA
		"""
		#check to see if we are applying a thresholding to preprocess the image
		"""if args.preprocess == "thresh" :
		"""	#gray = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		#gray = cv2.threshold(gray, 0, 256, cv2.THRESH_OTSU)[1]
		"""
		#make a check to see if median blurring should be done to remove noise
		elif args.preprocess=="blur":
			gray = cv2.medianBlur(gray,3)
		"""	
		#write the image file temporarily to disk so we can OCR it with the pytesseract interface, accessing
		# the (natively Java) tesseract application 

		#filename = "{}.png".format(os.getpid())
		#cv2.imwrite(filename,gray)


		#we can finally apply tesseract to the saved image using python bindings, while removing the temp image from memory
		text = pytesseract.image_to_string(gray)
		#print(text)
		#os.remove(filename)
		output_strings.append(text)
		os.remove(image_name)
		#cv2.imshow("Image",image)
		#cv2.imshow("Output", gray)
	return "".join(output_strings)
