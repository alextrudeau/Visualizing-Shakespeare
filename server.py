import os
import xml.etree.ElementTree
import operator
from flask import Flask, render_template, request, url_for, json, jsonify

#Initiate Flask app
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def root():
	return render_template('index.html')

# Get play page content for given play
@app.route('/get_play_content', methods=["POST"])
def get_play_content():
	if request.method == "POST":
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, 'static', "plays/json/" + request.data + ".json")
		data = json.load(open(json_url))
		return jsonify(data)

# Get word frequencies for a play for the word cloud visualization
@app.route('/get_word_frequencies', methods=["POST"])
def get_word_frequencies():
	if request.method == "POST":
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, 'static', "visualizations/wordCloud/json/" + request.data + ".json")
		data = json.load(open(json_url))
		return jsonify(data)

#Get a character's sides for a specific play and act/scene
@app.route('/get_character_sides', methods=["POST"])
def get_character_sides():
	if request.method == "POST":
		data = request.data.split("&")
		play = data[0][5:]
		character = data[1][10:]
		act = data[2][4:]
		scene = int_to_roman(data[3][6:])
		
		response = get_sides(play, character, act, scene)                                    
		return jsonify(response)

##############################################

# Functions for getting a character's sides

# JSON -> XML file name mappings
filenames = {
	"Ant": "a_and_c" ,  "AWW": "all_well",
	"AYL": "as_you"  ,  "Err": "com_err" ,
	"Cor": "coriolan",  "Cym": "cymbelin",
	"MND": "dream"   ,  "Ham": "hamlet"  ,
	"H41": "hen_iv_1",  "H42": "hen_iv_2",
	"H5": "hen_v"    ,  "H61": "hen_vi_1",
	"H62": "hen_vi_2",  "H63": "hen_vi_3",
	"H8": "hen_viii" ,  "JC": "j_caesar" ,
	"Jn": "john"     ,  "Lr": "lear"	 , 
	"LLL": "lll"     ,  "MM": "m_for_m"  , 
	"Wiv": "m_wives" ,  "Mac": "macbeth" ,
	"MV": "merchant" ,  "Ado": "much_ado",
	"Oth": "othello" ,  "Per": "pericles",
	"Rom": "r_and_j" ,  "R2": "rich_ii"  ,
	"R3": "rich_iii" ,  "TN": "t_night"  ,
	"Shr": "taming"  ,  "Tmp": "tempest" ,
	"Tim": "timon"   ,  "Tit": "titus"   ,
	"Tro": "troilus" ,  "TGV": "two_gent",
	"WT": "win_tale"
}

def int_to_roman(scene):
	conv = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
			[ 100, 'C'], [ 90, 'XC'], [ 50, 'L'], [ 40, 'XL'],
			[  10, 'X'], [  9, 'IX'], [  5, 'V'], [  4, 'IV'],
			[   1, 'I']]
	number = int(scene)
	result = ''
	for denom, roman_digit in conv:
		result += roman_digit*(number/denom)
		number %= denom
	return result

def get_sides(play, character, act_selected, scene_selected):
	relpath = "./xml/" + filenames[play] + ".xml"
	filename = os.path.join(os.path.dirname(__file__), relpath)
	e = xml.etree.ElementTree.parse(filename).getroot()

	total_lines = []
	total_prev_lines = []
	total_prev_characters = []
	for act in e.iter("ACT"):
		if act[0].text == ("ACT " + act_selected):
			for scene in act.iter("SCENE"):
				# The scene we're interested in
				if ("SCENE " + scene_selected + ".") in scene[0].text:
					for i in range(len(list(scene))):
						if scene[i].tag == "SPEECH":
							speech = scene[i]
							if speech.find("SPEAKER").text == (character):
								lines = []
								prev_lines = [] # The previous character's lines
								for line in speech.iter("LINE"):
									lines.append(line.text)
								if i > 0 and scene[i-1].tag == "SPEECH":
									numLines = len(list(scene[i-1])) - 1
									# If there are stage directions
									if not scene[i-1][numLines].text:
										line_words = []
										for text in scene[i-1][numLines].itertext():
											line_words.append(text.lstrip())
										prev_lines.insert(0, ": ".join(line_words))
									else:
										prev_lines.insert(0, scene[i-1][numLines].text)

									# Find previous character, if applicable
									total_prev_characters.append(scene[i-1].find("SPEAKER").text)

									# Find previous lines, until first capitalized line
									for j in range(numLines-1, 0, -1):
										prev_lines.insert(0, scene[i-1][j].text)
										if not scene[i-1][j].text:
											line_words = []
											for text in scene[i-1][j].itertext():
												line_words.append(text.lstrip())
											prev_lines.insert(0, " ".join(line_words))
										elif scene[i-1][j].text[0].isupper():
											break	
								else:
									prev_lines.append(scene[i-1].text)
									total_prev_characters.append("Stage Directions")
								total_lines.append(lines)
								total_prev_lines.append(prev_lines)
	return [total_lines, total_prev_lines, total_prev_characters]

##############################################

if __name__ == "__main__":

	app.run(debug=True)