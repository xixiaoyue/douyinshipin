import json
import os
import re

import aiofiles

from config import Config
import aiohttp
import asyncio

from xunfei import RequestApi


async def async_http_get(mode,text):
    pattern = r'https://\S+'
    url = re.findall(pattern, text)[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as response:
            # return response.url, await response.text()
            # await  response.text()
            redirect_url = str(response.url)
            if 'video' not in redirect_url:
                exit("链接并不是标准的分享链接！！")
        match = re.search(r'/video/(\d+)', redirect_url)
        video_id = match.group(1)
        u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(video_id)
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
        }
        async with session.get(url=u_id,headers=header, allow_redirects=True) as response:
            v_rs = await response.json()
            titles = v_rs['item_list'][0]['desc']
            req = v_rs['item_list'][0]['video']['play_addr']['uri']
        print(titles)
        v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
        async with session.get(url=v_url, headers=header, allow_redirects=True) as response:
            video = await response.read()
        async with aiofiles.open(fr'video\{titles}', 'wb') as file:
            await file.write(video)
        api = RequestApi(appid=Config.read_conf('config', 'appid'),
                         secret_key=Config.read_conf('config', 'secret_key'),
                         upload_file_path=fr'video\{titles}')

        v_text = await api.get_result()
        v_content = ''
        json_object = json.loads(v_text['content']['orderResult'])
        for j in json_object['lattice']:
            json_object = json.loads(j['json_1best'])
            for i in json_object['st']['rt'][0]['ws']:
                v_content+=i['cw'][0]['w']
        if mode==1:
            print(f"{titles}提取完毕！！！")
            return v_content
        else:
            async with aiofiles.open(fr'text\{titles}.txt', 'wt', encoding='utf-8') as file:
                await file.write(v_content)
            print(f"{titles}提取完毕！！！")



async def async_batch_http_get(line,text):
    pattern = r'https://\S+'
    url = re.findall(pattern, text)[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as response:
            # return response.url, await response.text()
            # await  response.text()
            redirect_url = str(response.url)
            if 'video' not in redirect_url:
                exit("链接并不是标准的分享链接！！")
        match = re.search(r'/video/(\d+)', redirect_url)
        video_id = match.group(1)
        u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(video_id)
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
        }
        async with session.get(url=u_id,headers=header, allow_redirects=True) as response:
            v_rs = await response.json()
            titles = v_rs['item_list'][0]['desc'].strip()
            req = v_rs['item_list'][0]['video']['play_addr']['uri']
        print(titles)
        v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
        async with session.get(url=v_url, headers=header, allow_redirects=True) as response:
            video = await response.read()
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {Config.read_conf('config', 'open_ai_key')}"  # 使用f-string格式化字符串
        }

        # FILE_PATH = "video\\" + path
        data = aiohttp.FormData()
        data.add_field('file', video, filename='test.mp4')
        data.add_field('model', 'whisper-1')
        data.add_field('response_format', 'text')

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data, timeout=aiohttp.ClientTimeout(total=60),
                                    proxy=f"http://{Config.read_conf('config', 'proxy')}") as response:
                d_text =  await response.text()
        async with aiofiles.open(fr'video\{titles}', 'a', encoding='utf-8') as file:
            await file.write(d_text)

        print(fr'{line}以及爬取完毕！！！')



if __name__ == '__main__':
    # 使用 asyncio 运行主程序
    text = "8.79 hOx:/ X@m.qe 08/12 GPT4V让效率提升的同时，某个职业的前途也黯淡了下去 GPT4V的统治力开始显现 # GPT # chatgpt # 知识领航者 者 # 科技新范式 https://v.douyin.com/iR93dAVx/ 复制此链接，打开Dou音搜索，直接观看视频！"
    a = asyncio.run(async_http_get(1,text))
    print(a)
    # Config.read_conf('config', 'open_ai_key')