import os
import re
import requests
from whisper import trans_text

def video(url):
    match = re.search(r'/video/(\d+)', url)
    video_id = match.group(1)
    # print(video_id)
    u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(video_id)
    header = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
    }

    v_rs = requests.get(url=u_id, headers=header).json()
    # print(v_rs['item_list'][0]['desc'])
    titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(0).strip()
    # print(titles)
    req = v_rs['item_list'][0]['video']['play_addr']['uri']
    v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
    v_req = requests.get(url=v_url, headers=header).content
    if not os.path.exists('video'):
        os.makedirs('video')
    with open(f'video/{titles}.mp4', 'wb') as f:
        f.write(v_req)
    print(f'{titles}视频下载成功！！')
    return titles

if __name__ == '__main__':
    while 1:
        text = input("请输入抖音的分享链接:")
        # text = "8.79 hOx:/ X@m.qe 08/12 GPT4V让效率提升的同时，某个职业的前途也黯淡了下去 GPT4V的统治力开始显现 # GPT # chatgpt # 知识领航者 者 # 科技新范式 https://v.douyin.com/iR93dAVx/ 复制此链接，打开Dou音搜索，直接观看视频！"
        # 使用修正后的正则表达式提取链接
        pattern = r'https://\S+'
        url = re.findall(pattern, text)[0]
        response = requests.get(url=url)
        url = response.url
        if 'video' not in url:
            exit("链接并不是标准的分享链接！！")
        titlle = video(url)
        text = trans_text(path=f'{titlle}.mp4')
        if not os.path.exists('text'):
            os.makedirs('text')
        with open(fr'text\{titlle}.txt','wt') as f:
            f.write(text)
        print(fr'{titlle}的脚本保存成功！！')