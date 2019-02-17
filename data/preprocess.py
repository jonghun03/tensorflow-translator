# damhiya
import numpy as np
import hgtk
import hgtk.const as hgc
import string

jamos = [(c,0) for c in hgc.CHO] + [(c,1) for c in hgc.JOONG] + [(c,2) for c in hgc.JONG]

char_list = string.printable[:-5] + jamos + ['‘', '’', 'ELSE', 'NONE', 'EOS']
char_dict = {char_list[i]:i for i in range(len(char_list))}

def decompose_ko(str):
    converted=[]
    for char in str:
        if hgtk.checker.is_hangul(char):
            jamos = hgtk.letter.decompose(char)
            indexes = list(range(len(jamos)))
            converted.extend(list(zip(jamos, indexes)))
        else:
            converted.append(char)

    return converted

def convert_str(str):
    str_conv = []

    for char in str:
        if char in char_dict:
            str_conv.append(char_dict[char])
        else:
            str_conv.append(char_dict['ELSE'])
    
    return str_conv

# en2ko
# EN     CHAR CHAR CHAR EOS  NONE NONE NONE
# KO     NONE NONE NONE CHAR CHAR CHAR EOS
def pack_en2ko(str_en, str_ko):
    str_en_pack = []
    str_ko_pack = []

    en_none_len = len(str_ko_pack)
    ko_none_len = len(str_en_pack)
    
    str_en_pack = str_en_pack + [char_dict['EOS']] + [char_dict['NONE']]*en_none_len
    str_ko_pack = [char_dict['NONE']]*ko_none_len + str_ko_pack + [char_dict['EOS']]

    return (str_en_conv, str_ko_conv)

# ko2en
# KO     CHAR CHAR CHAR EOS  NONE NONE NONE
# EN     NONE NONE NONE CHAR CHAR CHAR EOS
def pack_ko2en(str_ko, str_en):
    str_ko_conv = []
    str_en_conv = []

    ko_none_len = len(str_en_conv)
    en_none_len = len(str_ko_conv)
    
    str_ko_conv = str_ko_conv + [char_dict['EOS']] + [char_dict['NONE']]*ko_none_len
    str_en_conv = [char_dict['NONE']]*en_none_len + str_en_conv + [char_dict['EOS']]
    
    return (str_ko_conv, str_en_conv, len(str_en_conv))

# ‘You were both wonderful!’ ‘So were you!’ we said, returning the compliment.      (80)
# “당신 두 사람 다 정말 멋졌어요!” “당신들도 그랬어요!” 우리도 그렇게 말하며 같이 칭찬을 해 주었다.   (100*3)
# cat food (8)
# 고양이 먹이 (13)

def parse_file(file):
    seq64   = []
    seq128  = []
    seq256  = []
    seq512  = []
    seq1024 = []

    for line in file:
        _strs = line.split('|')
        str_en = convert_str(list(_strs[0]))
        str_ko = convert_str(decompose_ko(_strs[1][:-1]))

        length = len(str_en) + len(str_ko) + 1

        if length <= 64:
            seq64.append((str_en, str_ko))
        elif length <= 128:
            seq128.append((str_en, str_ko))
        elif length <= 256:
            seq256.append((str_en, str_ko))
        elif length <= 512:
            seq512.append((str_en, str_ko))
        elif length <= 1024:
            seq1024.append((str_en, str_ko))
        else:
            print("String length over : ")
            print(str_en)
            print(str_ko)

    x_en2ko_64   = np.empty((len(seq64), 64))
    y_en2ko_64   = np.empty((len(seq64), 64))

    x_ko2en_64   = np.empty((len(seq64), 64))
    y_ko2en_64   = np.empty((len(seq64), 64))

    x_en2ko_128  = np.empty((len(seq128), 128))
    y_en2ko_128  = np.empty((len(seq128), 128))

    x_ko2en_128  = np.empty((len(seq128), 128))
    y_ko2en_128  = np.empty((len(seq128), 128))

    x_en2ko_256  = np.empty((len(seq256), 256))
    y_en2ko_256  = np.empty((len(seq256), 256))

    x_ko2en_256  = np.empty((len(seq256), 256))
    y_ko2en_256  = np.empty((len(seq256), 256))

    x_en2ko_512  = np.empty((len(seq512), 512))
    y_en2ko_512  = np.empty((len(seq512), 512))

    x_ko2en_512  = np.empty((len(seq512), 512))
    y_ko2en_512  = np.empty((len(seq512), 512))

    x_en2ko_1024 = np.empty((len(seq1024), 1024))
    y_en2ko_1024 = np.empty((len(seq1024), 1024))

    x_ko2en_1024 = np.empty((len(seq1024), 1024))
    y_ko2en_1024 = np.empty((len(seq1024), 1024))

    x_en2ko_64[:]   = char_dict['NONE']
    y_en2ko_64[:]   = char_dict['NONE']

    x_ko2en_64[:]   = char_dict['NONE']
    y_ko2en_64[:]   = char_dict['NONE']

    x_en2ko_128[:]  = char_dict['NONE']
    y_en2ko_128[:]  = char_dict['NONE']

    x_ko2en_128[:]  = char_dict['NONE']
    y_ko2en_128[:]  = char_dict['NONE']

    x_en2ko_256[:]  = char_dict['NONE']
    y_en2ko_256[:]  = char_dict['NONE']

    x_ko2en_256[:]  = char_dict['NONE']
    y_ko2en_256[:]  = char_dict['NONE']

    x_en2ko_512[:]  = char_dict['NONE']
    y_en2ko_512[:]  = char_dict['NONE']

    x_ko2en_512[:]  = char_dict['NONE']
    y_ko2en_512[:]  = char_dict['NONE']

    x_en2ko_1024[:] = char_dict['NONE']
    y_en2ko_1024[:] = char_dict['NONE']

    x_ko2en_1024[:] = char_dict['NONE']
    y_ko2en_1024[:] = char_dict['NONE']

    for i in range(len(seq64)):
        str_en, str_ko = seq64[i]
        
        for j in range(len(str_en)):
            x_en2ko_64[i,j] = str_en[j]
        x_en2ko_64[i,len(str_en)] = char_dict['EOS']

        for j in range(len(str_ko)):
            y_en2ko_64[i,len(str_en)+j] = str_ko[j]
        y_en2ko_64[i,len(str_en)+len(str_ko)] = char_dict['EOS']

        for j in range(len(str_ko)):
            x_ko2en_64[i,j] = str_ko[j]
        x_ko2en_64[i,len(str_ko)] = char_dict['EOS']

        for j in range(len(str_en)):
            y_ko2en_64[i,len(str_ko)+j] = str_en[j]
        y_ko2en_64[i,len(str_ko)+len(str_en)] = char_dict['EOS']

    for i in range(len(seq128)):
        str_en, str_ko = seq128[i]
        
        for j in range(len(str_en)):
            x_en2ko_128[i,j] = str_en[j]
        x_en2ko_128[i,len(str_en)] = char_dict['EOS']

        for j in range(len(str_ko)):
            y_en2ko_128[i,len(str_en)+j] = str_ko[j]
        y_en2ko_128[i,len(str_en)+len(str_ko)] = char_dict['EOS']

        for j in range(len(str_ko)):
            x_ko2en_128[i,j] = str_ko[j]
        x_ko2en_128[i,len(str_ko)] = char_dict['EOS']

        for j in range(len(str_en)):
            y_ko2en_128[i,len(str_ko)+j] = str_en[j]
        y_ko2en_128[i,len(str_ko)+len(str_en)] = char_dict['EOS']
    
    for i in range(len(seq256)):
        str_en, str_ko = seq256[i]
        
        for j in range(len(str_en)):
            x_en2ko_256[i,j] = str_en[j]
        x_en2ko_256[i,len(str_en)] = char_dict['EOS']

        for j in range(len(str_ko)):
            y_en2ko_256[i,len(str_en)+j] = str_ko[j]
        y_en2ko_256[i,len(str_en)+len(str_ko)] = char_dict['EOS']

        for j in range(len(str_ko)):
            x_ko2en_256[i,j] = str_ko[j]
        x_ko2en_256[i,len(str_ko)] = char_dict['EOS']

        for j in range(len(str_en)):
            y_ko2en_256[i,len(str_ko)+j] = str_en[j]
        y_ko2en_256[i,len(str_ko)+len(str_en)] = char_dict['EOS']
    
    for i in range(len(seq512)):
        str_en, str_ko = seq512[i]
        
        for j in range(len(str_en)):
            x_en2ko_512[i,j] = str_en[j]
        x_en2ko_512[i,len(str_en)] = char_dict['EOS']

        for j in range(len(str_ko)):
            y_en2ko_512[i,len(str_en)+j] = str_ko[j]
        y_en2ko_512[i,len(str_en)+len(str_ko)] = char_dict['EOS']

        for j in range(len(str_ko)):
            x_ko2en_512[i,j] = str_ko[j]
        x_ko2en_512[i,len(str_ko)] = char_dict['EOS']

        for j in range(len(str_en)):
            y_ko2en_512[i,len(str_ko)+j] = str_en[j]
        y_ko2en_512[i,len(str_ko)+len(str_en)] = char_dict['EOS']
    
    for i in range(len(seq1024)):
        str_en, str_ko = seq1024[i]
        
        for j in range(len(str_en)):
            x_en2ko_1024[i,j] = str_en[j]
        x_en2ko_1024[i,len(str_en)] = char_dict['EOS']

        for j in range(len(str_ko)):
            y_en2ko_1024[i,len(str_en)+j] = str_ko[j]
        y_en2ko_1024[i,len(str_en)+len(str_ko)] = char_dict['EOS']

        for j in range(len(str_ko)):
            x_ko2en_1024[i,j] = str_ko[j]
        x_ko2en_1024[i,len(str_ko)] = char_dict['EOS']

        for j in range(len(str_en)):
            y_ko2en_1024[i,len(str_ko)+j] = str_en[j]
        y_ko2en_1024[i,len(str_ko)+len(str_en)] = char_dict['EOS']

    return (((x_en2ko_64, y_en2ko_64), (x_en2ko_128, y_en2ko_128), (x_en2ko_256, y_en2ko_256),
                (x_en2ko_512, y_en2ko_512), (x_en2ko_1024, y_en2ko_1024)),
            ((x_ko2en_64, y_ko2en_64), (x_ko2en_128, y_ko2en_128), (x_ko2en_256, y_ko2en_256),
                (x_ko2en_512, y_ko2en_512), (x_ko2en_1024, y_ko2en_1024)))