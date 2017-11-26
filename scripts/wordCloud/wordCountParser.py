# Created by Jane Wu
# Parser that reads in XML files of the plays and stores frequency of words in the plays
import xml.etree.ElementTree
import sys
import operator
import os
import json

#NLP library to ignore stop words, i.e. "and", "the", etc.
from nltk.corpus import stopwords

filenames = {
    "a_and_c": "Ant" ,  "all_well": "AWW",
    "as_you": "AYL"  ,  "com_err": "Err" ,
    "coriolan": "Cor",  "cymbelin": "Cym",
    "dream": "MND"   ,  "hamlet": "Ham"  ,
    "hen_iv_1": "H41",  "hen_iv_2": "H42",
    "hen_v": "H5"    ,  "hen_vi_1": "H61",
    "hen_vi_2": "H62",  "hen_vi_3": "H63",
    "hen_viii": "H8" ,  "j_caesar": "JC" ,
    "john":"Jn"      ,  "lear": "Lr"     , 
    "lll": "LLL"     ,  "m_for_m": "MM"  , 
    "m_wives": "Wiv" ,  "macbeth": "Mac" ,
    "merchant": "MV" ,  "much_ado": "Ado" ,
    "othello": "Oth" ,  "pericles": "Per",
    "r_and_j": "Rom" ,  "rich_ii": "R2"  ,
    "rich_iii": "R3" ,  "t_night": "TN"  ,
    "taming": "Shr"  ,  "tempest": "Tmp" ,
    "timon": "Tim"   ,  "titus": "Tit"   ,
    "troilus": "Tro" ,  "two_gent": "TGV",
    "win_tale": "WT"
}

# Common words across plays
commonWords = []
for play in filenames:
	relpath = "../../xml/" + play + ".xml"
	filename = os.path.join(os.path.dirname(__file__), relpath)
	print filename
	e = xml.etree.ElementTree.parse(filename).getroot()

	# Dictionary with key: word, value: word count
	wordCounts = {}
	# Format for D3
	frequency_list = []

	# Common Shakespeare words
	shakespeareStopWords = []
	with open("stopwords.txt") as f:
	    shakespeareStopWords = f.readlines()
	for i in range(len(shakespeareStopWords)):
		shakespeareStopWords[i] = shakespeareStopWords[i].strip("\n")


	for scene in e.iter("SCENE"):
		for speech in scene.iter("SPEECH"):
			for line in speech.iter("LINE"):
				if not line.text:
					continue
				words = [word.lower().replace(",","")
					.replace(".","")
					.replace("?","")
					.replace("!","")
					.replace("--","")
					.replace("'s","")
					.replace(";","")
					.replace(":","")
					for word in line.text.split()]
				for word in words:
					if (word not in stopwords.words('english')) and (word not in shakespeareStopWords):
						if not (word in wordCounts):
							wordCounts[word] = 1
						else:
							wordCounts[word] += 1
	
	sorted_list = sorted(wordCounts.items(), key=operator.itemgetter(1))
	sorted_list = sorted_list[-50:]
	print sorted_list


	for word in wordCounts:
		if (word, wordCounts[word]) in sorted_list:
			frequency_list.append({"text":word,"size":wordCounts[word]})

	# Write result to file
	relpath = "json/" + filenames[play] + ".json"
	output_file = os.path.join(os.path.dirname(__file__), relpath)
	print output_file
	with open(output_file, 'w') as outfile:
	    json.dump(frequency_list, outfile)


		




