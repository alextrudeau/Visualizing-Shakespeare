
# Created by Jane Wu slightly added to by Anthony Romm
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
	relpath = "../xml/" + play + ".xml"
	filename = os.path.join(os.path.dirname(__file__), relpath)
	print filename
	e = xml.etree.ElementTree.parse(filename).getroot()

	# Dictionary with key: word, value: word count
	wordCounts = {}
	# Format for D3
	frequency_list = {}
	charColorMap = {}
	
	for scene in e.iter("SCENE"):
		for speech in scene.iter("SPEECH"):
			for speaker in speech.iter("SPEAKER"):
			
				char = speaker.text
				charColorMap[char] = 0
	
	charCount = len(charColorMap)
	marginalColor = 360*1.0/charCount
	color = 0
	
	for character in charColorMap:
		charColorMap[character] = str(color)
		color += marginalColor
	

	print charColorMap
	# Common Shakespeare words
	shakespeareStopWords = []
	with open("wordCloud/stopwords.txt") as f:
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
			frequency_list[word] = 0
			
	# find location in file. store in json with theme: nature,lord,.. character:name quote: the line its on? can be improve to maybe search back for a period and search forward for one or something. location: act # scene #
	actCount = 1
	sceneCount = 1
	character = ""
	themes = ""
	quote = ""
	json_list = []
	
	for act in e.iter("ACT"):
		for scene in act.iter("SCENE"):
			for speech in scene.iter("SPEECH"):
				for speaker in speech.iter("SPEAKER"):
					character = speaker.text
				for line in speech.iter("LINE"):
					if not line.text:
						continue
					for word in frequency_list:
						lineWords = line.text.replace(",", " ").replace(".", " ").replace(";", " ").replace("?", " ").replace("!"," ").replace("'s", " ").replace("--", " ").split(" ")
						if word in lineWords or word.capitalize() in lineWords or (word + "s") in lineWords:
							themes += word + ","
							quote = line.text
				
					try:
						color = charColorMap[character]
					except KeyError:
						color = "0"
						
					json_list.append({"theme":themes,"character":character,"quote":quote,"act":actCount,"scene":sceneCount, "color":color})
					themes = ""
					quote = ""
					
			sceneCount += 1
		actCount += 1
		sceneCount = 1


	# Write result to file
	relpath = "../static/visualizations/themeGraph/json/" + filenames[play] + ".json"
	output_file = os.path.join(os.path.dirname(__file__), relpath)
	print output_file
	with open(output_file, 'w') as outfile:
	    json.dump(json_list, outfile)


		


