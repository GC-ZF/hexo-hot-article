"""
@Author:张时贰
@Date:2022年12月21日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
import os

import uvicorn
from fastapi import FastAPI
from Blog_Statistics.Post_Table import run_api
from fastapi.responses import HTMLResponse
from Blog_Statistics.Spider_Post import by_parsel_replace, csdn
from Blog_Statistics.Screen_Shot import save_img
from fastapi.responses import FileResponse
from Site_Analytics.baidu.baidu import baidu_get_token, baidu_refresh_token, get_hot_article, \
    get_visitor_province, get_visitor_counrty

app = FastAPI ()


@app.get ( "/", response_class=HTMLResponse )
async def deploy():
    '''
    部署成功返回信息
    :return:
    '''
    html = """
    <div style="text-align:center;margin:0 auto;line-height:500px;">
			<p>部署成功，请按照仓库说明使用</p>
	</div>
    """
    return html


@app.get ( '/favicon.ico' )
async def favicon():
    '''
    浏览器图标
    :return:
    '''
    path = os.path.dirname ( os.path.dirname ( os.path.realpath ( __file__ ) ) )
    favicon_path = path + '/static/ico.jpg'
    return FileResponse ( favicon_path )


@app.get ( "/all/" )
async def all(url: str = '域名/get_all?url=博客地址'):
    '''
    获取博客所有文章信息
    :param url: 博客url
    :return: title、link、time组成的一个列表字典
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '博客地址为' + url )
    title_link_time_list = await run_api ( url )
    return title_link_time_list


@app.get ( "/get_article/", response_class=HTMLResponse )
async def get_article(url: str = '域名/get_post?url=文章地址'):
    '''
    获取单篇文章信息
    :param url: 文章地址
    :return: 文章内容
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '文章地址为' + url )
    html = by_parsel_replace ( url )
    return html


@app.get ( "/get_baidu_token/" )
async def get_baidu_token(API_Key: str, Secret_Key: str, CODE: str):
    '''
    获取百度token
    :param API_Key: 百度账号API_Key
    :param Secret_Key: 百度账号Secret_Key
    :param CODE: 登录并访问 http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={你的API_Key}&redirect_uri=oob&scope=basic&display=popup
    :return: {'access_token': access_token, 'refresh_token': refresh_token}
    '''
    return baidu_get_token ( API_Key, Secret_Key, CODE )


@app.get ( "/get_baidu_refresh/" )
async def get_baidu_refresh(API_Key: str, Secret_Key: str, refresh_token: str):
    '''
    通过 refresh_token 刷新百度token
    :param API_Key: 百度账号API_Key
    :param Secret_Key: 百度账号Secret_Key
    :param refresh_token: 百度账号refresh_token
    :return: {'access_token': access_token, 'refresh_token': refresh_token}
    '''
    return baidu_refresh_token ( API_Key, Secret_Key, refresh_token )


@app.get ( "/get_hot_article/" )
async def get_hot_articles(access_token: str, url: str):
    '''
    获取博客热文统计
    :param access_token: 百度分析access_token
    :param domain: 博客域名
    :return: 以pv排序返回文章标题、链接、pv、uv、平均时长
    '''
    return get_hot_article ( access_token, url )


@app.get ( "/visitor_province/" )
async def get_visitor_provinces(access_token: str, url: str):
    '''
    获取访客省份统计
    :param access_token: 百度分析access_token
    :param domain: 博客域名
    :return: 博客访客省份的UV
    '''
    return get_visitor_province ( access_token, url )


@app.get ( "/get_visitor_counrty/" )
async def get_visitor_counrtys(access_token: str, url: str):
    '''
    获取访客国家统计
    :param access_token: 百度分析access_token
    :param domain: 博客域名
    :return: 博客访客国家的UV
    '''
    return get_visitor_counrty ( access_token, url )


@app.get ( "/screen/", response_class=HTMLResponse )
async def screen(url: str = '域名/screen?url=网址'):
    '''
    获取网址截图
    :param url: 网址
    :return: img
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '网址为' + url )
    base64 = save_img ( url )
    html = f'<img src="data:image/png;base64,{base64}" />'
    return html


@app.get ( "/csdn/", response_class=HTMLResponse )
async def spider_csdn(url: str = '域名/screen?url=网址'):
    '''
    爬取CSDN
    :param url: CSDN文章链接
    :return:
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '网址为' + url )
    html = csdn ( url )
    return html


if __name__ == '__main__':
    uvicorn.run ( "index:app", host="0.0.0.0", reload=True )
    # uvicorn.run (app, host="0.0.0.0" )
    # uvicorn index:app --reload
