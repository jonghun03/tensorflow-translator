#jh030512
import mecab 
import re

Mecab = mecab.MeCab()

def read_data(file):
    str_pairs = []
    for line in file:
        [en_str, ko_str] = line[:-1].split('|')

        str_pairs.append((ko_str, en_str))

    return str_pairs

def convert_string(morph):
    string = morph
    single = re.compile('‘|’|「|」|〈|〉')
    double = re.compile('“|”')
    thin_space = re.compile(' ')
    digits = re.compile('\d')
    dash = re.compile('─')
    other = re.compile("\’\,")

    if digits.match(string) or other.match(string):
        return list(single.sub('', string))
    elif single.match(string):
        return [single.sub('\'', string)]
    elif double.match(string):
        return [double.sub('"', string)]
    elif dash.match(string):
        return [dash.sub('-', string)]
    elif thin_space.match(string):
        return None
    else:
        return [string]

def ko_parser(string):
    morphs = []
    outputs = Mecab.morphs(string.lower())

    for morph in outputs:
        converted = convert_string(morph)
        if converted != None:
            morphs.extend(converted)

    return morphs

def en_parser(string):
    morphs = []
    outputs = Mecab.morphs(string.lower())

    for morph in outputs:
        converted = convert_string(morph)
        if converted != None:
            morphs.extend(converted)

    return morphs