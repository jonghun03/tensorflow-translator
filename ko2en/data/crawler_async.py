# jh030512
import re
import asyncio
import aiohttp as request
import aiofiles as files
from bs4 import BeautifulSoup

with open("source_url.txt", 'r') as urlfile:
    url = [line[:-1] for line in urlfile]

with open('data_crawler.txt', 'w', encoding="utf-8") as init:
    init.write('')

async def load_words():
    async with files.open('keys.txt', 'r') as keys:
        data = await keys.readlines()
        if data:
            return {value[:-1] for value in data}
        else:
            print('keys.txt 파일에 단어가 없습니다!')
            raise Exception

async def search(word):
    async with request.ClientSession() as sess:
        async with sess.get(url[0] + word + url[1]) as res:
            return await res.text()

async def get_result(real_url):
    async with request.ClientSession() as sess:
        async with sess.get(url[3] + real_url) as res:
            return await res.text()

async def write(dict):
    async with files.open('data_crawler.txt', 'a+', encoding="utf-8") as file:
            if await file.read() != '':
                await file.write('\n')
            for k, v in dict.items():
                await file.write(k + '|' + v + '\n')

async def main():
    words = await load_words()
    for word in words:
        searched = await search(word)
        searched_soup = BeautifulSoup(searched, 'html.parser')
        try:
            real_url = searched_soup.select(url[2])[0].get('href')
            article = await get_result(real_url)
            article_soup = BeautifulSoup(article, 'html.parser')
            misc_filter = re.compile('<.+?>|\s?\(.+?\)\s?|\s?\[.+?\]\s?|[\\r\\n\\t]+|\s{3,}')
            special_chars = re.compile('.+?/.+?|".+?|\'.+?\'')

            english, korean = article_soup.select(url[4]), article_soup.select(url[5])
            english_filtered = [misc_filter.sub('', str(english[i])) for i in range(len(english)) if misc_filter.sub('', str(english[i]))]
            korean_filtered = [misc_filter.sub('', str(korean[i])) for i in range(len(korean)) if misc_filter.sub('', str(korean[i]))]
            dicts = await write({english_filtered[i]: korean_filtered[i] for i in range(len(english_filtered)) if not special_chars.match(english_filtered[i])})
        except:
            continue
        no_special = re.compile('.*?\'.*?|.*?’.*?|.*?‘.*?|.*?/.*?|.*?\-.*?|.*?\d.*?|.*?\—.*?|.*?;.*?|.*?“.*?|.*?….*?|.*?─.*?')
        for i in range(len(english_filtered)):
            splitted = [ re.sub('\.|,|\?|\!|”|:', '', i.lower()) for i in english_filtered[i].split() if not no_special.match(i) ]
            for j, v in enumerate(splitted):
                wrds = await load_words()
                if not (v in wrds):
                    await addword(v)
    

    

    