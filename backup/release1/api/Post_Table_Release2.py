"""
@Author:张时贰
@Date:2022年12月16日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
import json
import sqlite3

'''
相对于Release1 简化了一丢丢代码 加了aiohttp做异步，但是效果并不明显，快了0.5s
'''
import time
from lxml import etree
import requests
import asyncio
import aiohttp


# 获取博客页数
def get_page_num(blog_url):
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
    return page_num


# request无法异步，换用aiohttp库做异步请求
async def requests_get(link):
    async with aiohttp.ClientSession () as session:
        async with session.get ( link ) as resp:
            try:
                text = await resp.text ()
                return text
            except Exception as e:
                e = str ( e )
                print ( f'请求状态码{resp.status}，错误：{e}' )


# 抓取博客文章的 标题 链接
async def get_info(url):
    html = await requests_get ( url )
    html = etree.HTML ( html )
    title_list = html.xpath ( '//*[@class="recent-post-info"]/a/@title' )
    link_list = html.xpath ( '//*[@class="recent-post-info"]/a/@href' )
    # time_list = html.xpath ( '//*[@class="post-meta-date-created"]/text()' ) # 博客未开启更新于时不适用
    time_list = html.xpath ( '//*[@class="post-meta-date-created"]/text()' )
    if len(time_list)==0:
        time_list = html.xpath ( '//*[@class="post-meta-date"]/time/text()' )
    post_num = len ( title_list )  # 文章数
    link_title_list = [ ]
    for i in range ( post_num ):
        title = title_list[ i ]
        link = link_list[ i ]
        time = time_list[ i ]
        tmp = {"title": title, "link": blog_url + link, "time": time}
        link_title_list.append ( tmp )
    return link_title_list


def run(site_url):
    global blog_url
    blog_url=site_url
    page_num = int ( get_page_num ( blog_url ) )  # 博客页数
    # 如果博客只有一页
    if page_num.__eq__ ( 1 ):
        # 创建协程容器（获取事件循环）
        # loop = asyncio.get_event_loop ()
        loop = asyncio.new_event_loop ()
        asyncio.set_event_loop ( loop )
        # 指定协程添加任务
        tasks = [ asyncio.ensure_future ( get_info ( blog_url ) ) ]
        # 运行任务（将所有的事件对象传入事件循环）
        loop.run_until_complete ( asyncio.wait ( tasks ) )
    # 如果博客多于1页
    else:
        # 创建协程容器（获取事件循环）
        # loop = asyncio.get_event_loop ()
        loop = asyncio.new_event_loop ()
        asyncio.set_event_loop ( loop )
        # 指定协程添加任务
        tasks = [ asyncio.ensure_future ( get_info ( blog_url ) ) ]  # 第一页
        for i in range ( 1, page_num ):
            tasks.append ( asyncio.ensure_future ( get_info ( f'{blog_url}/page/{i + 1}/#content-inner' ) ) )
        # 运行任务（将所有的事件对象传入事件循环）
        loop.run_until_complete ( asyncio.wait ( tasks ) )

    # 将异步返回值合并
    link_title = [ ]  # 列表字典：链接 文章标题 发布于
    for task in tasks:
        link_title = link_title + task.result ()
    link_title = sorted ( link_title, key=lambda x: x[ 'time' ], reverse=True )  # 解决因为异步导致的乱序，按时间降序
    return link_title


# 写入md文件
def save_md(row, post_info):
    with open ( 'Post_Table.md', 'w', encoding='utf-8' ) as f:
        for i in range ( row ):
            f.write ( '| Post ' )
        f.write ( '| \n' )
        for i in range ( row ):
            f.write ( '| :----: ' )
        f.write ( '| \n' )
        tmp = 0
        for line in post_info:
            tmp = tmp + 1
            title = f'| [{line[ "title" ]}]({line[ "link" ]}) '
            f.write ( title )
            if row.__eq__ ( tmp ):
                f.write ( '| \n' )
                tmp = 0


# 写入json文件
def save_json(post_info):
    with open ( 'Post_Table.json', 'w', encoding='utf-8' ) as f:
        f.write ( json.dumps ( post_info, indent=4, ensure_ascii=False ) )


# 写入db
def save_sql(post_info):
    # 将字典转集合，方便后续去重批量执行sql语句
    link_title_set = set ()
    for i in post_info:
        tmp = (i[ 'title' ], i[ 'link' ], i[ 'time' ])
        link_title_set.add ( tmp )

    connect = sqlite3.connect ( 'Blog_Post.db' )  # 连接数据库
    sql = connect.cursor ()  # 创建cursor对象
    # sql.execute ( "DROP TABLE IF EXISTS Blog_Post" )
    sql.execute ( "CREATE TABLE if NOT EXISTS Blog_Post( title text PRIMARY KEY, link text, time text)" )

    # 去重
    link_title_table = sql.execute ( "SELECT * FROM Blog_Post" ).fetchall ()
    link_title_table = set ( link_title_table )
    link_title_set = link_title_set - link_title_table

    # 插入文章数据
    # sql.execute (
    #     "INSERT INTO Blog_Post VALUES( '2022 11 13 月亮还是那个月亮','https://zhangshier.vip/posts/53805/','2022-11-13 00:10:24')" )
    sql.executemany ( 'INSERT INTO Blog_Post(title,link,time) VALUES(  ?, ?, ?)', link_title_set )

    connect.commit ()
    connect.close ()


# 对api做的接口
def get_json(blog_url):
    page_num = int ( get_page_num ( blog_url ) )  # 博客页数

    link_title = [ ]  # 构造字典：链接 文章标题
    run ( page_num, blog_url )  # 异步抓取
    link_title = sorted ( link_title, key=lambda x: x[ 'time' ], reverse=True )  # 解决因为异步导致的乱序，按时间降序
    return link_title


if __name__ == '__main__':
    start = time.time ()
    # blog_url = 'https://zhangshier.vip'  # 博客地址
    # blog_url = 'https://blog.panghai.top'  # 博客地址
    blog_url = 'https://luomengguo.top'  # 博客地址
    # blog_url = 'https://tzy1997.com'  # 博客地址
    # blog_url = 'https://blog.leonus.cn'  # 博客地址
    # blog_url = 'https://www.chuckle.top'  # 博客地址
    # blog_url = 'https://anzhiy.cn'  # 博客地址

    row = 4  # 输出md文件列数
    link_title = run ( blog_url )  # 异步抓取

    # save_json ( link_title )  # 写入json文件
    # save_md ( row, link_title )  # 写入md文件
    # save_sql ( link_title )  # 写入sql文件
    print ( time.time () - start )
