import util

def load_dict(file):
    return {word[:-1] : i for i, word in enumerate(file)}

def generate_buckets(str_pairs, ko_dict, en_dict):
    buckets = [[],[],[]]
    for ko_str, en_str in str_pairs:
        ko_morphs = util.ko_parser(ko_str)
        en_morphs = util.en_parser(en_str)

        ko_encoded = [ko_dict[morph] for morph in ko_morphs]
        en_encoded = [en_dict[morph] for morph in en_morphs]

        ko_encoded.append(ko_dict['EOS'])
        en_encoded.append(en_dict['EOS'])

        ko_len = len(ko_encoded)
        en_len = len(en_encoded)

        if ko_len <= 8 and en_len <= 8:
            buckets[0].append((ko_encoded, en_encoded))
        elif ko_len <= 16 and en_len <= 16:
            buckets[1].append((ko_encoded, en_encoded))
        elif ko_len <= 32 and en_len <= 32:
            buckets[2].append((ko_encoded, en_encoded))
        else:
            print("sentence length out of range!")
    
    print(len(buckets[0]))
    print(len(buckets[1]))
    print(len(buckets[2]))


if __name__ == '__main__':
    ko_dict_file = open("ko_dict.txt")
    en_dict_file = open("en_dict.txt")
    data = open("data_crawler.txt")

    ko_dict = load_dict(ko_dict_file)
    en_dict = load_dict(en_dict_file)

    str_pairs = util.read_data(data)

    buckets = generate_buckets(str_pairs, ko_dict, en_dict)