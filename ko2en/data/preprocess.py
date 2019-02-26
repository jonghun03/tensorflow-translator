import numpy as np
import util
import pickle

def load_dict(file):
    return {word[:-1] : i for i, word in enumerate(file)}

def pyl2nparr(pyl, size, pad):
    nparr = np.zeros(size, dtype='int32')
    nparr[:] = pad

    for i,x in enumerate(pyl):
        nparr[i] = pyl[i]

    return nparr


def generate_buckets(str_pairs, ko_dict, en_dict):
    buckets_pyl = [[],[],[],[]]
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
            buckets_pyl[0].append((ko_encoded, en_encoded))
        elif ko_len <= 16 and en_len <= 16:
            buckets_pyl[1].append((ko_encoded, en_encoded))
        elif ko_len <= 32 and en_len <= 32:
            buckets_pyl[2].append((ko_encoded, en_encoded))
        elif ko_len <= 64 and en_len <= 64:
            buckets_pyl[3].append((ko_encoded, en_encoded))
        else:
            print("sentence length out of range!")
    
    print(len(buckets_pyl[0]))
    print(len(buckets_pyl[1]))
    print(len(buckets_pyl[2]))
    print(len(buckets_pyl[3]))

    buckets_nparr = [[], [], [], []]

    size = 8

    for bucket_pyl, bucket_nparr in zip(buckets_pyl, buckets_nparr):
        bucket_nparr.append(np.zeros([0,size], dtype='int32'))
        bucket_nparr.append(np.zeros([0,size], dtype='int32'))

        for ko_pyl, en_pyl in bucket_pyl:
            ko_nparr = pyl2nparr(ko_pyl, size, ko_dict['PAD']).reshape([1,size])
            en_nparr = pyl2nparr(en_pyl, size, en_dict['PAD']).reshape([1,size])

            bucket_nparr[0] = np.append(bucket_nparr[0], ko_nparr, axis=0)
            bucket_nparr[1] = np.append(bucket_nparr[1], en_nparr, axis=0)

        size *= 2

    return buckets_nparr


if __name__ == '__main__':
    ko_dict_file = open("ko_dict.txt")
    en_dict_file = open("en_dict.txt")
    data = open("data_crawler.txt")

    ko_dict = load_dict(ko_dict_file)
    en_dict = load_dict(en_dict_file)

    str_pairs = util.read_data(data)

    buckets = generate_buckets(str_pairs, ko_dict, en_dict)

    pickle.dump(buckets, open('buckets.pk', 'wb'))