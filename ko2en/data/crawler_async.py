# jh030512
import re
import asyncio
import aiohttp as request
import aiofiles as files
from bs4 import BeautifulSoup

# TODO : key_new.txt 에 새 키 저장, 이미 쓴 키는 key_used.txt 에 저장
# 단어 목록 자동 추가
auto_add_key = True

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

async def write(key_dict):
    async with files.open('data_crawler.txt', 'a+', encoding="utf-8") as file:
            if await file.read() != '':
                await file.write('\n')
            for k, v in key_dict.items():
                await file.write(k + '|' + v + '\n')

async def addword(word):
    async with files.open('keys.txt', 'a+', encoding="utf-8") as kys:
            if await kys.read() != '':
                await kys.write('\n')
            await kys.write(word + '\n')

async def main():
    words = await load_words()
    for word in words:
        try:
            article = BeautifulSoup(await get_result(BeautifulSoup(await search(word), 'html.parser').select(url[2])[0].get('href')), 'html.parser')
            misc_filter, special_chars = re.compile('<.+?>|\s?\(.+?\)\s?|\s?\[.+?\]\s?|[\\r\\n\\t]+|\s{3,}'), re.compile('.+?/.+?|".+?|\'.+?\'')
            english, korean = article.select(url[4]), article.select(url[5])
            english_filtered = [misc_filter.sub('', str(english[i])) for i in range(len(english)) if misc_filter.sub('', str(english[i]))]
            korean_filtered = [misc_filter.sub('', str(korean[i])) for i in range(len(korean)) if misc_filter.sub('', str(korean[i]))]
            dicts = await write({english_filtered[i]: korean_filtered[i] for i in range(len(english_filtered)) if not special_chars.match(english_filtered[i])})
        except:
            continue
        no_special = re.compile('.*?\'.*?|.*?’.*?|.*?‘.*?|.*?/.*?|.*?\-.*?|.*?\d.*?|.*?\—.*?|.*?;.*?|.*?“.*?|.*?….*?|.*?─.*?|.*?°.*?')

        if auto_add_key:
            for i in range(len(english_filtered)):
                splitted = [ re.sub('\.|,|\?|\!|”|:', '', i.lower()) for i in english_filtered[i].split() if not no_special.match(i) ]
                for j, v in enumerate(splitted):
                    wrds = await load_words()
                    if not (v in wrds):
                        await addword(v)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())