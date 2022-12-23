"""
@Author:张时贰
@Date:2022年12月15日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
import time
import requests
from lxml import etree

start = time.time ()
blog_url = 'https://zhangshier.vip'  # 博客地址
# blog_url = 'https://blog.panghai.top'  # 博客地址
# blog_url = 'https://luomengguo.top'  # 博客地址
# blog_url = 'https://tzy1997.com'  # 博客地址
# blog_url = 'https://blog.leonus.cn'  # 博客地址
# blog_url = 'https://www.chuckle.top'  # 博客地址
# blog_url = 'https://anzhiy.cn'  # 博客地址
row = 4  # 输出文件列数

r = requests.get ( blog_url )
r = r.content.decode ( 'utf-8' )
html = etree.HTML ( r )

# 获取博客页数
try:
    page_num = html.xpath ( '//*[@class="pagination"]/a[2]//text()' )[ 0 ]  # 博客页数
except IndexError as e:
    try:
        e = str ( e )
        print ( "error:" + e + "，博客页数较少没有 <span class=\"space\">…</span>" )
        page_num = html.xpath ( '//*[@class="pagination"]/a//text()' )[ 0 ]  # 博客页数
    except Exception as e:
        e = str ( e )
        print ( "error:" + e + "，博客只有一页" )
        page_num = 1
# string = etree.tostring(element_, encoding='utf-8').decode('utf-8')     # etree转html
# print(string)
page_num = int ( page_num )
link_title = [ ]  # 构造字典：链接 文章标题

for i in range ( page_num ):
    # 第一页
    if i.__eq__ ( 0 ):
        url = blog_url  # 博客地址
        r = requests.get ( url )
        r = r.content.decode ( 'utf-8' )
        html = etree.HTML ( r )
        # post_num = html.xpath ( '//*[@id="recent-posts"]/div' )  # 有的人魔改的贡献图和置顶轮播图页用id="recent-posts"注册，实际上并不是文章
        post_num = html.xpath ( '//*[@class="recent-post-info"]' )  # 当前页的文章数
        post_num = len ( post_num )
        for i in range ( post_num ):
            title = html.xpath ( '//*[@class="recent-post-info"]/a/@title' )[ i ]
            link = html.xpath ( '//*[@class="recent-post-info"]/a/@href' )[ i ]
            tmp = {"title": title, "link": blog_url + link}
            link_title.append ( tmp )
    # 其它页
    else:
        url = f'{blog_url}/page/{i + 1}/#content-inner'
        r = requests.get ( url )
        r = r.content.decode ( 'utf-8' )
        html = etree.HTML ( r )
        post_num = html.xpath ( '//*[@class="recent-post-info"]' )  # 当前页的文章数
        post_num = len ( post_num )
        for i in range ( post_num ):
            title = html.xpath ( '//*[@class="recent-post-info"]/a/@title' )[ i ]
            link = html.xpath ( '//*[@class="recent-post-info"]/a/@href' )[ i ]
            tmp = {"title": title, "link": blog_url + link}
            link_title.append ( tmp )

with open ( 'Post_Table.md', 'w', encoding='utf-8' ) as f:
    for i in range ( row ):
        f.write ( '| Post ' )
    f.write ( '| \n' )
    for i in range ( row ):
        f.write ( '| :----: ' )
    f.write ( '| \n' )
    tmp = 0
    for line in link_title:
        tmp = tmp + 1
        title = f'| [{line[ "title" ]}]({line[ "link" ]}) '
        f.write ( title )
        if row.__eq__ ( tmp ):
            f.write ( '| \n' )
            tmp = 0

print ( time.time () - start )
