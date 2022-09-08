import re
import os

import requests


def start(url):
    sec_uid = re.findall('user/(.*)\?', url)[0]  # 从url中提取sec_uid
    max_cursor = '0'  # 初始max_cursor
    quantity = 0  # 初始视频数量
    while True:
        data = requests.get(
            f'https://m.douyin.com/web/api/v2/aweme/post/?reflow_source=reflow_page&sec_uid={sec_uid}&count=21&max_cursor={max_cursor}').json()  # 请求数据
        max_cursor = data['max_cursor']  # 获取max_cursor
        aweme_list = data['aweme_list']  # 获取视频列表
        for aweme in aweme_list:  # 遍历视频列表
            quantity += 1  # 视频数量+1
            video_name = aweme['desc']  # 获取视频名称
            video_url = aweme['video']['play_addr']['url_list'][0]  # 获取视频地址
            nickname = aweme['author']['nickname']  # 获取作者昵称
            print(f'正在下载第{quantity}个视频：{video_name}')  # 打印视频名称
            video_name = video_name.replace('\n', ' ')  # 吧\n替换成空格
            if video_name == '':
                video_name = str(quantity) + nickname  # 如果视频名称为空，就用视频数量+作者昵称作为视频名称
            if not os.path.exists(f'./{nickname}'):  # 如果作者文件夹不存在，就创建
                os.mkdir(f'./{nickname}')  # 如果作者文件夹不存在，就创建一个
            with open(f'./{nickname}/{video_name}.mp4', 'wb') as f:
                f.write(requests.get(video_url).content)
        has_more = data['has_more']
        if not has_more:  # 如果has_more为False 说明没有更多视频了
            break  # 退出循环
    print(f'共下载{quantity}个视频')


if __name__ == '__main__':
    url = input(
        '请输入作者主页链接：')  # 输入作者主页链接 例：https://www.douyin.com/user/MS4wLjABAAAAm-YgirNQo_9nm1B8TNynOD5ZrYBtesVrgBuaZaS2dzQ?vid=6907843457583205646
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }
    url = requests.get(url, headers=headers).url  # 获取重定向后的url
    start(url)