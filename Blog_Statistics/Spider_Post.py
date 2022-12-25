import multiprocessing
import os
import random
import threading
import time
import html2text
import requests
import parsel
import time
from multiprocessing import Pool
import datetime

'''
需求分析：通过给定链接获取页面html并转为markdown保存
遇到问题：当蝴蝶主题开启懒加载，img标签中src不等于实际地址
三种思路，经测试方案三用时最短，主要浏览器加载请求资源太多了，这个不可控
'''
# 因为vercel不支持selenium，此文件selenium部分全部注释
# from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# def add_options():
#     # 创建谷歌浏览器驱动参数对象
#     chrome_options = webdriver.ChromeOptions ()
#     # 不加载图片
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     chrome_options.add_experimental_option ( "prefs", prefs )
#     # 使用无界面浏览器模式！！
#     chrome_options.add_argument ( '--headless' )
#     # 使用隐身模式（无痕模式）
#     chrome_options.add_argument ( '--incognito' )
#     # 禁用GPU加速
#     chrome_options.add_argument ( '--disable-gpu' )
#     return chrome_options
#
#
# def by_selenium_value(link):
#     '''
#     方案一：利用selenium库，img标签外包裹了a标签，a标签中有img的实际地址，通过dom操作将a.src给img.href
#     :param link: 文章链接
#     :return:
#     '''
#     # 1、创建浏览器对象 - 打开浏览器
#     driver = webdriver.Chrome ()  # 本地调试打开浏览器窗口
#     driver.maximize_window ()
#     # driver = webdriver.Chrome ( options=add_options () )  # 不开启浏览器的情况下调试
#     # 2、打开博文
#     driver.get ( link )
#     # 3、找到所有a、img标签
#     a_list = driver.find_elements ( By.XPATH, '//*[@id="article-container"]/p/a/img/..' )
#     # 4、替换所有的img.href=a.src
#     for i in range ( len ( a_list ) ):
#         a_href = a_list[ i ].get_attribute ( 'href' )
#         js = f"document.querySelectorAll('.post-content p img')[{i}].src = '{a_href}'"
#         driver.execute_script ( js )
#     # 5、获取文章内容部分的HTML
#     post_content = driver.find_element ( By.XPATH, '//*[@id="article-container"]' ).get_attribute ( 'outerHTML' )
#     post_title = driver.find_element ( By.CSS_SELECTOR, '.post-title' ).get_attribute ( 'innerHTML' )
#
#     # 6、二次处理
#     # 蝴蝶主题代码框用table绘制分为行号（.gutter）和代码区域（.code） table标签转md会生成 '---'，解决： 用replace去除table，遍历去除<td class="gutter">xxx</td>
#     post_content = post_content.replace ( '<table><tbody><tr><td class="gutter">',
#                                           '<tbody><tr><td class="gutter">' )  # 主题配置代码不换行情况匹配规则 code_word_wrap: false
#     post_content = post_content.replace ( '<table><tbody><tr><td class="code">',
#                                           '<tbody><tr><td class="code">' )  # 主题配置代码不换行情况匹配规则 code_word_wrap: true
#     # 去除 .gutter
#     tmp = driver.find_elements ( By.CSS_SELECTOR, '.gutter' )
#     code_span = [ ]  # 找出所有的.gutter标签
#     for i in tmp:
#         code_span.append ( i.get_attribute ( 'outerHTML' ) )
#     for i in code_span:
#         post_content = post_content.replace ( i, '' )
#
#     # 7、保存markdown
#     # markdown = html2text.html2text ( post_content )
#     #
#     # path = os.path.dirname ( __file__ )
#     # path = path + '/by_selenium_value'
#     # if not os.path.exists ( path ):
#     #     os.mkdir ( path )
#     #
#     # with open ( f'{path}/{post_title}.md', 'w', encoding='utf-8' ) as file:
#     #     file.write ( markdown )
#
#
# def by_selenium_scroll(link):
#     '''
#     方案二：利用selenium库，img标签外包裹了a标签，找到所有的img的上一级a，滚动到a让图片加载（直接找图片会造成滚动坐标越界）
#     :param link: 文章链接
#     :return:
#     '''
#     # 1、创建浏览器对象 - 打开浏览器
#     driver = webdriver.Chrome ()  # 本地调试打开浏览器窗口
#     driver.maximize_window ()
#     # driver = webdriver.Chrome ( options=add_options () )  # 不开启浏览器的情况下调试
#     # 2、打开博文
#     driver.get ( link )
#     # 3、找到所有图片外包裹的a
#     img_list = driver.find_elements ( By.XPATH, '//*[@id="article-container"]/p/a/img/..' )
#     # img_list = driver.find_elements ( By.CSS_SELECTOR, '#article-container p a' )
#     # 4、滚动到图片位置
#     for img in img_list:
#         ActionChains ( driver ).scroll_to_element ( img ).perform ()
#     # 5、获取文章内容部分的HTML
#     post_content = driver.find_element ( By.XPATH, '//*[@id="article-container"]' ).get_attribute ( 'outerHTML' )
#     post_title = driver.find_element ( By.CSS_SELECTOR, '.post-title' ).get_attribute ( 'innerHTML' )
#
#     # 6、二次处理
#     # 蝴蝶主题代码框用table绘制分为行号（.gutter）和代码区域（.code） table标签转md会生成 '---'，解决： 用replace去除table，遍历去除<td class="gutter">xxx</td>
#     post_content = post_content.replace ( '<table><tbody><tr><td class="gutter">',
#                                           '<tbody><tr><td class="gutter">' )  # 主题配置代码不换行情况匹配规则 code_word_wrap: false
#     post_content = post_content.replace ( '<table><tbody><tr><td class="code">',
#                                           '<tbody><tr><td class="code">' )  # 主题配置代码不换行情况匹配规则 code_word_wrap: true
#     # 去除 .gutter
#     tmp = driver.find_elements ( By.CSS_SELECTOR, '.gutter' )
#     code_span = [ ]  # 找出所有的.gutter标签
#     for i in tmp:
#         code_span.append ( i.get_attribute ( 'outerHTML' ) )
#     for i in code_span:
#         post_content = post_content.replace ( i, '' )
#
#     # 7、保存markdown
#     # markdown = html2text.html2text ( post_content )
#     # path = os.path.dirname ( __file__ )
#     # path = path + '/by_selenium_scroll'
#     # if not os.path.exists ( path ):
#     #     os.mkdir ( path )
#     #
#     # with open ( f'{path}/{post_title}.md', 'w', encoding='utf-8' ) as file:
#     #     file.write ( markdown )


def by_parsel_replace(link):
    '''
    方案叁：利用parsel库，img标签中 src和data-lazy-src替换： <img src="懒加载编码" data-lazy-src="实际地址" alt="" style="">
    :param link: 文章链接
    :return:
    '''
    # 1、爬取html代码
    request = requests.get ( link )
    html = request.content.decode ( 'utf-8' )
    select = parsel.Selector ( html )

    # 2、获取文章标题和内容
    post_title = select.css ( '.post-title::text' ).get ()
    post_content = select.css ( '.post-content' ).get ()

    # 3、处理懒加载图片
    post_content = post_content.replace ( 'src', 'lazy' ).replace ( 'data-lazy-lazy', 'src' )  # 处理图片

    # 4、处理多余的标签
    # 蝴蝶主题代码框用table绘制分为行号（.gutter）和代码区域（.code） table标签转md会生成 '---'，解决： 用replace去除table，遍历去除<td class="gutter">xxx</td>
    # 去<table>
    post_content = post_content.replace ( '<table><tr><td class="gutter">',
                                          '<tr><td class="gutter">' )  # 主题配置代码不换行情况匹配规则 code_word_wrap: false
    post_content = post_content.replace ( '<table><tr><td class="code">',
                                          '<tr><td class="code">' )  # 主题配置代码不换行情况匹配规则 code_word_wrap: true

    # 去行号 当蝴蝶主题使用代码框换行时，代码框是单独的一个td标签，用replace处理掉
    code_span = select.css ( '.gutter' ).getall ()
    for i in code_span:
        post_content = post_content.replace ( i, '' )

    # 5、转md
    markdown = html2text.html2text ( post_content )
    # with open ( f'by_parsel_replace/{post_title}.md', 'w', encoding='utf-8' ) as file:
    #     file.writelines ( markdown )

    # 6、去代码框前多余的换行
    markdown = markdown.split ( '\n' )
    file_content = [ ]
    for i in range ( len ( markdown ) ):
        if (markdown[ i ].__eq__ ( '    ' ) or markdown[ i ].__eq__ ( '      ' )):
            continue
        else:
            file_content.append ( markdown[ i ] + '\n' )
    # 7、保存文件
    # path = os.path.dirname ( __file__ )
    # path = path + '/by_parsel_replace'
    # if not os.path.exists ( path ):
    #     os.mkdir ( path )
    # print ( file_content )
    # with open ( f'{path}/{post_title}.md', 'w', encoding='utf-8' ) as file:
    #     for i in file_content:
    #         file.write ( i )
    return post_content


def csdn(link):
    '''
    爬取CSDN
    :param link: 文章链接
    :return:
    '''
    # (.*?):(.*)
    # "$1":"$2",
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
        "Referer": "https://blog.csdn.net/tansty_zh"
    }
    request = requests.get ( link, headers=headers )
    html = request.text
    select = parsel.Selector ( html )
    post_content = select.css ( '#article_content' ).get ()
    post_title = select.css ( '.title-article::text' ).get ()
    markdown = html2text.html2text ( post_content )

    # 可能因为CSDN防盗机制，，html2text无法直接解析图片地址被分开 '![在这里插入图片描述](https://img-\n', 'blog.csdnimg.cn/90d.png#pic_center)\n'
    # with open ( f'{post_title}.md', 'w', encoding='utf-8' ) as file:
    #     file.write (markdown)

    # 解决办法
    markdown = markdown.split ( '\n' )
    file_content = [ ]
    flag = 0

    for i in range ( len ( markdown ) - 1 ):
        # 如果是空说明换行，插入一个换行
        if (markdown[ i ].__eq__ ( '    ' )):
            # file_content.append ( '\n' )
            continue
        # 如果包含 '](https://img-' 说明下一次循环是后半个图片地址，flag作为标记
        # img_pattern = re.compile(r'^!\[.*', re.M)
        # img_pattern=img_pattern.match(content).group()
        elif '](https://img-' in markdown[ i ]:
            flag = 1
            img_front_url = markdown[ i ]
        # flag==1 说明这次循环是图片的后半段地址
        elif flag == 1:
            flag = 0
            file_content.append ( img_front_url + markdown[ i ] + '\n' )
        # 否则就是单纯的文本内容
        else:
            file_content.append ( markdown[ i ] + '\n' )

    # path = os.path.dirname ( __file__ )
    # path = path + '/CSDN'
    # if not os.path.exists ( path ):
    #     os.mkdir ( path )
    #
    # with open ( f'{path}/{post_title}.md', 'w', encoding='utf-8' ) as file:
    #     for i in file_content:
    #         file.write ( i )
    return post_content


if __name__ == '__main__':
    url = 'https://zhangshier.vip/posts/7884/'
    # url = 'https://zhangshier.vip/posts/53805/'

    # print ( 'by_selenium_value运行时长：' )
    # start = time.time ()
    # by_selenium_value ( url )
    # print ( time.time () - start )
    #
    # print ( 'by_selenium_scroll运行时长：' )
    # start = time.time ()
    # by_selenium_scroll ( url )
    # print ( time.time () - start )

    # print ( 'by_parsel_replace运行时长：' )
    # start = time.time ()
    # by_parsel_replace ( url )
    # print ( time.time () - start )

    # url = 'https://blog.csdn.net/qq_49488584/article/details/126884686?spm=1001.2014.3001.5502'
    # print ( 'csdn爬取运行时长：' )
    # start = time.time ()
    # csdn ( url )
    # print ( time.time () - start )

    # url=[('https://zhangshier.vip/posts/7339/',),
    #      ('https://zhangshier.vip/posts/53805/',),
    #      ('https://zhangshier.vip/posts/26324/',)]
    #
    # start = time.time ()
    # thread1 = threading.Thread ( name='t1', target=by_selenium_value, args=url[0] )
    # thread2 = threading.Thread ( name='t2', target=by_selenium_value, args=url[1] )
    # thread3 = threading.Thread ( name='t3', target=by_selenium_value, args=url[2] )
    #
    # thread1.start ()
    # thread1.join()
    # thread2.start ()
    # thread2.join ()
    # thread3.start ()
    # thread3.join ()
    # print ( time.time () - start )
    #
    # start = time.time ()
    # po=Pool(3)
    # url = [ 'https://zhangshier.vip/posts/7339/',
    #         'https://zhangshier.vip/posts/53805/',
    #         'https://zhangshier.vip/posts/26324/' ]
    # po.map( by_selenium_value, url )
    # po.close ()  # 关闭进程池，不再接受新的进程
    # po.join ()  # 主进程阻塞等待子进程的退出
    # print ( time.time () - start )
