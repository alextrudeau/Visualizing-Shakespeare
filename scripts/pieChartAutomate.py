import json
import csv

filenames = ["Ant", "AWW", "AYL", "Err", "Cor", "Cym", "MND", "Ham", "H41", "H42", "H5", "H61", "H62", "H63", "H8", "JC", "Jn", "Lr",
"LLL", "MM", "Wiv", "Mac", "MV", "Ado", "Oth", "Per", "Rom", "R2", "R3", "TN", "Shr", "Tmp", "Tim", "Tit", "Tro", "TGV", "WT"]

# d3.hsl

for play in filenames:
	json_data = open(play + ".json").read()

	themes = json.loads(json_data)

	themeDic = {}
	characterColor = {}

	for line in themes:
		themeL = line["theme"].split(",")

		if line["character"] not in characterColor:
			characterColor[line["character"]] = line["color"]
		
		for theme in themeL:
			if theme != "":
				if str(theme) not in themeDic:
					themeDic[str(theme)] = {}
					themeDic[str(theme)][str(line["character"])] = 1
				elif str(line["character"]) not in themeDic[str(theme)]:
					themeDic[str(theme)][str(line["character"])] = 1
				else:
					themeDic[str(theme)][str(line["character"])] += 1

	numEntries = {}
	maxLen = 0
	for word in themeDic:
		numEntries[word] = len(themeDic[word])
		maxLen = max(maxLen, len(themeDic[word]))

	table = [[" " for i in range(3*len(numEntries))] for j in range(maxLen)]

	themeCounter = 0
	characterCounter = 0
	for theme in themeDic:
		for character in themeDic[theme]:
			table[characterCounter][themeCounter*3] = character
			table[characterCounter][themeCounter*3 + 1] = str(themeDic[theme][character])
			table[characterCounter][themeCounter*3 + 2] = characterColor[character]
			characterCounter += 1
		characterCounter = 0
		themeCounter += 1

	with open(play + '.csv', 'wb') as csvfile:
	    themeS = ""

	    for theme in themeDic:
	    	themeS += theme + "," + theme + "Lines," + theme + "Color,"
	    themeS = themeS[:-1]
	    themeS += "\n"
	    csvfile.write(themeS)

	    for row in table:
	    	csvString = ""
	    	for element in row:
	    		csvString += element + ","
	    	csvString = csvString[:-1]
	    	csvString += "\n"
	    	csvfile.write(csvString)



