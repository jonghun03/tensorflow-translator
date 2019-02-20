import util

def generate_dict(strings, parser):
    morph_dict = ['EOS']

    for string in strings:
        morphs = parser(string)

        for morph in morphs:
            if not morph in morph_dict:
                morph_dict.append(morph)

    return morph_dict

def save_dict(file, morph_dict):
    for morph in morph_dict:
        file.write(morph + '\n')

if __name__ == '__main__':
    data = open("data_crawler.txt")
    str_pairs = util.read_data(data)
    ko_strings, en_strings = tuple(zip(*str_pairs))

    ko_dict = generate_dict(ko_strings, util.ko_parser)
    en_dict = generate_dict(en_strings, util.en_parser)

    ko_dict_file = open("ko_dict.txt", 'w')
    en_dict_file = open("en_dict.txt", 'w')
    
    save_dict(ko_dict_file, ko_dict)
    save_dict(en_dict_file, en_dict)

    ko_dict_file.close()
    en_dict_file.close()

