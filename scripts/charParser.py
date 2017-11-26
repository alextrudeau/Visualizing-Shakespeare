import xml.etree.ElementTree
import sys

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

for arg in sys.argv:
    if arg == "scripts/charParser.py":
        continue  
    print arg
    slashIndex = arg.index("/")
    extensionIndex = arg.index(".xml")
    file = arg[slashIndex + 1: extensionIndex]
    filename = filenames[file]
    
    e = xml.etree.ElementTree.parse(arg).getroot()
    
    # chars: list of all characters; sceneChars: 2d list of characters per scene
    chars = []
    sceneChars = [[]]
    sceneCount = 0
    
    # Gather speakers per scene into 2d list
    for scene in e.iter("SCENE"):
        for speech in scene.iter("SPEECH"):
            for speaker in speech.iter("SPEAKER"):
                if speaker.text not in sceneChars[sceneCount]:
                    sceneChars[sceneCount] += [speaker.text]
                    if speaker.text not in chars:
                        chars += [speaker.text]
        sceneCount += 1
        sceneChars += [[]]
    
    # matrix: 2d list of integers; integer value = how often 2 characters speak
    # num scenes shared with:[ A,   B,   C,   D   ]
    # format:    character A [ 0,   1,   2,   0   ]
    #            character B [ 1,   0,   5,   2   ]
    #            character C [ 2,   5,   0,   1   ]
    #            character D [ 0,   2,   1,   0   ]
    #
    speakerCount = len(chars)
    matrix = []
    
    # prepopulate matrix with 0's (base value)
    for i in range(speakerCount):
        if i != speakerCount:
            matrix += [[]]    
        for j in range(speakerCount):
            matrix[i] += [0]
     
    # populate matrix with proper values
    for scene in sceneChars:
        for char1 in scene:
            for char2 in scene:
                index1 = chars.index(char1)
                index2 = chars.index(char2)
                if index1 != index2 :
                    matrix[index1][index2] += 1
    
    luminAddition = 75.0/len(chars)
    lumin = 20
    
    csv = ""
    
    csv += "name,color\n"
   
    print chars
    print file
    print "------------------------"
    for char in chars:
		char = char.split(" ")
		char = [c.capitalize() for c in char]
		char = " ".join(char)
		csv += char 
		csv +=  ",\"d3.hsl(185, 1, " 
		csv += str(lumin/100.0)
		csv += ")\"\n"
		lumin += luminAddition
       


    f = open("./static/visualizations/speakChord/csv/" + filename + ".csv", 'w+')
    f.write(csv)
    
    f = open("./static/visualizations/speakChord/matrix/" + filename + ".json", 'w+')
    f.write(str(matrix))

