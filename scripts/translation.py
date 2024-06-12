import os
import xml.etree.ElementTree as ET

import translators as ts

GAME_PATH = os.getcwd()

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
            strs_to_translate.update(
                {data.attrib[id_attr]: data.attrib[text_attr]}
            )
        else:
            print(f"WARNING! {text_attr} or {id_attr} is not in {data.attrib}")

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
                print(f"Unable to translate via KeyError: "
                      f"{error} in {data.attrib}")

    file.write(os.path.join(GAME_PATH, path), encoding="windows-1251")

    return True


def kk_lang_fix(phrases):
    kk_letters = {
        "Ә": "†",
        "ә": "‡",
        "Ғ": "‰",
        "ғ": "Љ",
        "Қ": "Њ",
        "қ": "Ќ",
        "Ң": "Ћ",
        "ң": "Џ",
        "Ө": "ђ",
        "ө": "љ",
        "Ұ": "њ",
        "ұ": "ќ",
        "Ү": "ћ",
        "ү": "џ",
        "Һ": "Ў",
        "һ": "ў"
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

        for k, v in SYMBOLS_TO_AVOID.items():
            for id, phrase in phrases.items():
                if k in phrase:
                    phrase = phrase.replace(k, v)
                    phrases.update({id: phrase})

    print(f"translating text data from {from_lang} to {to_lang}...")
    for id, phrase in phrases.items():
        translation = ts.translate_text(
            phrase,
            translator="google",
            from_language=from_lang,
            to_language=to_lang
        )
        phrases.update({id: translation})

    if to_lang == "kk":
        phrases = kk_lang_fix(phrases)

    if need_validation:
        for k, v in SYMBOLS_TO_AVOID.items():
            for id, phrase in phrases.items():
                if v in phrase:
                    phrase = phrase.replace(v, k)
                    phrases.update({id: phrase})

    print(f"applying changes to {path}...")
    if write(file, path, containers, phrases):
        print("DONE\n")
        return True


def main():
    # print(f"working in {GAME_PATH}")

    # with open("manifest.yaml") as manifest:
    #     FILES_TO_CHANGE = yaml.safe_load(manifest)

    # for file, cont in FILES_TO_CHANGE.items():
    #     translate(file, cont, to_lang="kk")

    translation = ts.translate_text(
        "Привет, мир!",
        translator="google",
        from_language="ru",
        to_language="kk"
    )
    print(kk_lang_fix({"id": translation}))


if __name__ == "__main__":
    main()
