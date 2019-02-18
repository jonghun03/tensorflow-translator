# jh030512
import re
import requests
from bs4 import BeautifulSoup

with open("source_url.txt", 'r') as urlfile:
    url = [line[:-1] for line in urlfile]

with open('keys.txt', 'r') as keys:
    data = keys.readlines()
    if data:
        words = {value[:-1] for value in data}
    else:
        print('keys.txt 파일에 단어가 없습니다!')
        raise Exception

with open('data_crawler.txt', 'w', encoding="utf-8") as initialize:
    initialize.write('')

for word in words:
    searched = requests.get(url[0] + word + url[1])
    searched_soup = BeautifulSoup(searched.content, 'html.parser')
    try:
        real_url = searched_soup.select(url[2])[0].get('href')
    except:
        continue
    endict = requests.get(url[3] + real_url)
    dict_soup = BeautifulSoup(endict.content, 'html.parser')
    misc_filter = re.compile('<.+?>|\s?\(.+?\)\s?|\s?\[.+?\]\s?|[\\r\\n\\t]+|\s{3,}')
    special_chars = re.compile('.+?/.+?|".+?|\'.+?\'')
    english, korean = dict_soup.select(url[4]), dict_soup.select(url[5])

    english_filtered = [misc_filter.sub('', str(english[i])) for i in range(len(english)) if misc_filter.sub('', str(english[i]))]
    korean_filtered = [misc_filter.sub('', str(korean[i])) for i in range(len(korean)) if misc_filter.sub('', str(korean[i]))]
    dicts = {english_filtered[i]: korean_filtered[i] for i in range(len(english_filtered)) if not special_chars.match(english_filtered[i])}

    with open('data_crawler.txt', 'a+', encoding="utf-8") as file:
        if file.read() != '':
            file.write('\n')

        for k, v in dicts.items():
            file.write(k + '|' + v + '\n')