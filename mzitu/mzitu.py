import os
import traceback

import requests
from bs4 import BeautifulSoup


def get_html_text(url, timeout=5):
    '模拟get请求，获取页面'
    try:
        r = requests.get(url)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def get_html_text_with_post(url, timeout=5):
    '''模拟post请求，获取页面'''
    try:
        r = requests.post(url)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'

#获取当前页面的所有图组url
def parse_url_list(url):
    url_list = []
    html = get_html_text_with_post(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # urls = soup.find_all('a', class_='list-link')
        urls = soup.find('ul',id='pins').find_all('li')
        for url in urls:
            # 针对 //www.yuemei.com/c/1711873.html 格式进行特殊处理
            url_list.append((url.a)['href'])
    else:
        print('错误发生了！')

    return url_list

#获取所有图片的url地址
def parse_img_package(url):
    img_list = []
    html = get_html_text(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 解析name
        pagenavi=soup.find('div',class_='pagenavi').find_all('a')
        #图组的名称
        name = soup.find('h2', class_='main-title').text
        #该组图片的数量
        count=int(pagenavi[-2].text)
        #解析图片的url并放到img——list中
        for i in (range(1,count)):
            pichtml=get_html_text(url+'/'+str(i))
            picsoup = BeautifulSoup(pichtml, 'lxml')
            picurl=picsoup.find('div',class_='main-image').find('img')['src']
            img_list.append(picurl)

        # 将名字和图片链接打包
        print('图组:{} 解析完毕'.format(name))
        return dict(urls=img_list, name=name)
    else:
        print(str(traceback.format_exc()))
        return 'error'


def img_downloader(package):
    dirname = BASE_DIR + 'imgs/' + package['name']
    # 创建对应的文件夹
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        # 开始下载图片
        for url in package['urls']:
            filename = url.split('/')[-1]
            open(dirname + '/' + filename, 'wb').write(requests.get(url).content)
            print('正在下载:{}'.format(filename))
        print('{}图组下载完毕！'.format(package['name']))
    else:
        print('该图包已经下载过了')


base_enter_url = 'http://www.mzitu.com/page/{}/'
enter_url_list = [base_enter_url.format(i) for i in range(1, 51)]
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'


if __name__ == '__main__':

    packages = []
    #所有图组的url
    diarys = parse_url_list(enter_url_list[0])

    for diary_url in diarys[0:2]:
        # 所有图片的url和名称
        package = parse_img_package(diary_url)
        if package != 'error':
            packages.append(package)

    # 开启多进程模式下载图片
    from multiprocessing import Pool
    # 建立进程池，我cpu是四核的，就是四个进程
    pool = Pool()
    # 进程池，开始批量下载
    pool.map(img_downloader, packages)
    pool.close()
    pool.join()