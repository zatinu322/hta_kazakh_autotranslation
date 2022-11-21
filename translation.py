import os
import translators as ts
import xml.etree.ElementTree as ET

GAME_PATH = os.getcwd()

FILES_TO_CHANGE = {
    # "data\\if\\dialogs\\credits.xml":           ["Page", "id", "text", False], 
    # "data\\if\\diz\\dialogsglobal.xml":         ["Reply", "name", "text", False], 
    # "data\\if\\diz\\dynamicdialogsglobal.xml":  ["Reply", "name", "text", True], 
    # "data\\if\\diz\\levelinfo.xml":             ["LevelInfo", "name", "fullName", False], 
    # "data\\if\\diz\\model_names.xml":           ["Item", "id", "value", False], 
    # "data\\if\\diz\\questinfoglobal.xml":       ["QuestInfo", "questName", "briefDiz", True], 
    "data\\if\\diz\\questinfoglobal.xml":       ["QuestInfo", "questName", "fullDiz", True], 
    # "data\\if\\strings\\affixesdiz.xml":        ["string", "id", "value", False], 
    # "data\\if\\strings\\bindnames.xml":         ["string", "id", "value", True], 
    # "data\\if\\strings\\clansdiz.xml":          ["string", "id", "value", False], 
    # "data\\if\\strings\\fadingmsgs.xml":        ["string", "id", "value", True], 
    # "data\\if\\strings\\gamestrings.xml":       ["string", "id", "value", True], 
    # "data\\if\\strings\\help.xml":              ["string", "id", "value", False], 
    # "data\\if\\strings\\objectdiz.xml":         ["string", "id", "value", False], 
    # "data\\if\\strings\\setupstrings.xml":      ["string", "id", "value", False], 
    # "data\\if\\strings\\statistics.xml":        ["string", "id", "value", False], 
    # "data\\if\\strings\\uibooks.xml":           ["string", "id", "value", False], 
    # "data\\if\\strings\\uidescription.xml":     ["string", "id", "value", False], 
    # "data\\if\\strings\\uieditorstrings.xml":   ["string", "id", "value", False], 
    # "data\\if\\strings\\uieditstrings.xml":     ["string", "id", "value", True], 
    # "data\\if\\strings\\uihistory.xml":         ["string", "id", "value", False], 
    # "data\\maps\\r1m1\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r1m1\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r1m2\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r1m2\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r1m3\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r1m3\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r1m4\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r1m4\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r3m1\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r3m1\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r3m2\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r3m2\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r2m1\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r2m1\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r2m2\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r2m2\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r4m1\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r4m1\\strings.xml":            ["string", "id", "value", False], 
    # "data\\maps\\r4m2\\object_names.xml":       ["Object", "Name", "FullName", False], 
    # "data\\maps\\r4m2\\strings.xml":            ["string", "id", "value", False], 
    # "data\\sounds\\radio\\radiosamples.xml":    ["Sample", "id", "text", False]
}

SYMBOLS_TO_AVOID = {
    "%1n": "123456781", 
    "%1s": "123456782", 
    "%1d": "123456783", 
    "%1m": "123456784", 
    "%1p": "123456785", 
    "%2n": "123456786", 
    "%2b": "123456787", 
    "%2d": "123456788", 
    "%3d": "123456789", 
    "%s": "123456780"
}

def parse(path):
    file = ET.parse(os.path.join(GAME_PATH, path))

    return file

def get_text(file_root, containers):
    strs_to_translate = {}

    tag = containers[0]
    id_attr = containers[1]
    text_attr = containers[2]

    for data in file_root.iter(tag):
        if id_attr and text_attr in data.attrib.keys():
            strs_to_translate.update({data.attrib[id_attr]: data.attrib[text_attr]})
        else:
            print(f"NONONO! {text_attr} or {id_attr} is not in data.attrib")
    
    return strs_to_translate

def write(file, path, containers, phrases):
    file_root = file.getroot()

    tag = containers[0]
    id_attr = containers[1]
    text_attr = containers[2]

    for data in file_root.iter(tag):
        if id_attr and text_attr in data.attrib.keys():
            try:
                data.set(text_attr, phrases[data.attrib[id_attr]])
            except KeyError as error:
                print(error)
    
    file.write(os.path.join(GAME_PATH, path), encoding="windows-1251")
    
    return True

def kk_lang_fix(phrases):
    kk_letters = {
        "Ә": "Э",
        "ә": "э",
        "Ғ": "F",
        "ғ": "f",
        "Қ": "K",
        "қ": "k",
        "Ң": "Н",
        "ң": "н",
        "Ө": "О",
        "ө": "о",
        "Ұ": "Y",
        "ұ": "y",
        "Ү": "Y",
        "ү": "y",
        "Һ": "h",
        "һ": "h"
        }
    for id, text in phrases.items():
        for word, change in kk_letters.items():
            if word in text:
                text = text.replace(word, change)
            phrases.update({id: text})
    
    return phrases

def translate(path, containers, from_lang="ru", to_lang="en"):
    print(f"parsing {path}...")
    file = parse(path)
    file_root = file.getroot()

    need_validation = containers[3]

    print(f"extracting text data from {path}...")
    phrases = get_text(file_root, containers)

    if need_validation:
        if "ExMachina URL" in phrases.keys():
            phrases.pop("ExMachina URL")
            phrases.pop("Buka URL")
            phrases.pop("Nival URL")
        
        for k,v in SYMBOLS_TO_AVOID.items():
            for id, phrase in phrases.items():
                if k in phrase:
                    phrase = phrase.replace(k, v)
                    phrases.update({id: phrase})

    print(f"translating text data from {from_lang} to {to_lang}...")
    for id, phrase in phrases.items():
        translation = ts.google(phrase, from_language=from_lang, to_language=to_lang)
        phrases.update({id: translation})

    if to_lang == "kk":
        phrases = kk_lang_fix(phrases)

    if need_validation:
        for k,v in SYMBOLS_TO_AVOID.items():
            for id, phrase in phrases.items():
                if v in phrase:
                    phrase = phrase.replace(v, k)
                    phrases.update({id: phrase})

    print(f"applying changes to {path}...")
    if write(file, path, containers, phrases):
        print("DONE\n")
        return True

def main():
    print(f"working in {GAME_PATH}")
    for file, cont in FILES_TO_CHANGE.items():
        # try:
        translate(file, cont, to_lang="kk")
        # except Exception as err:
        #     print(err)
    
if __name__ == "__main__":
    main()
