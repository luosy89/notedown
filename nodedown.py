import requests
import os
from lxml import etree
from multiprocessing import Pool
title_nove = ''
url_base = 'https://XXX'
def Chapterspider(url):
    """章节爬虫，参数传入目录，返回(章节名称， 对应页面链接)的列表"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    content = requests.get(url, headers=headers).content
    html = etree.HTML(content)
    chapter_title = html.xpath('//div[@id="info"]/h1/text()')
    title_nove = chapter_title[0]
    print("打印文件夹"+title_nove)
    try:
        os.makedirs(chapter_title[0])
        print(str(chapter_title)+'开始下载')
    except:
        print('已有'+str(chapter_title)+'文件夹')
    chapter_names = html.xpath('//dd/a/text()')
    chapter_links = html.xpath('//dd/a/@href')
    return chapter_names, chapter_links
def Chapterdownload(turple):
    """章节下载成对应的txt，这个url参数指每一页的链接，chapter_link"""
    url = turple[0]
    name = turple[1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    rsp = requests.get(url, headers=headers)
    content = rsp.content
    html = etree.HTML(content)
    # content_mame = html.xpath('//a[@href="https://www.xbiquge.la/7/7877/"]/text()')
    content_mame = html.xpath('//a[@href="https://www.xbiquge.la/32/32626/"]/text()')
    content_list = html.xpath('//div[@id="content"]//text()')
    content_list = Remove_r(content_list, "\r")
    content_list = Formatlist(content_list)[:-2]
    # os.chdir('斗破苍穹') 
    with open(content_mame[0]+'/'+name+'.txt', 'w', encoding='utf-8') as f:
        f.writelines(content_list)
    print(name, '爬取完毕')
def Remove_r(list, a):
    """去除列表中含字符串a的项"""
    while True:  # 无限循环，利用break退出
        if a not in list:  # 判断"a"在不在char_list里，不在就break。否则执行删除“a”的操作
            break
        else:
            list.remove(a)
    return list
def Formatlist(list):
    """去除只有/r的项后，还要把每项的特殊字符去掉     和\r"""
    for i in range(len(list)):
        if '\r' in list[i]:
            list[i] = list[i].replace('\r', '\n')
        if '\xa0\xa0\xa0\xa0' in list[i]:
            list[i] = list[i].replace('\xa0\xa0\xa0\xa0', '')
    return list
 
if __name__ == '__main__':
    chapter_links = []
    url = url_base  #这个是目录的链接，只需要填这个就行了，当前目录下自己手动创建一个叫小说的文件夹来存小说
    chapter_names, chapter_links_before = Chapterspider(url)
    for i, j in zip(chapter_names, chapter_links_before):
        j = 'http://'+url.split('/')[2]+j
        chapter_links.append(j)
    #生成链接和章名一一对应的字典
    link_find_name = dict(zip(chapter_links, chapter_names))
    canshu = []
    for link, name in link_find_name.items():
        canshu.append((link, name))
    # for ab in canshu:
    #     print(ab)
    pool = Pool(processes=32)
    pool.map(Chapterdownload, canshu)