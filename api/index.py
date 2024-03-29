import os
import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) )
sys.path.append ( BASE_DIR )
from Blog_Statistics.Post_Table import run_api
from Site_Analytics.baidu.baidu import baidu_get_token, baidu_refresh_token, get_hot_article, \
    get_visitor_province, get_visitor_counrty
from Site_Analytics.baidu.run import getToken
from Blog_Statistics.Spider_Post import by_parsel_replace, csdn
from Fork_Repo.github_calendar_api import get_calendar
from Fork_Repo.weibo_api import get_weibo

# from Blog_Statistics.Screen_Shot import save_img

app = FastAPI ()

app.add_middleware (
    CORSMiddleware,
    allow_origins=[ "*" ],
    allow_credentials=False,
    allow_methods=[ "*" ],
    allow_headers=[ "*" ],
)


@app.get ( "/", response_class=HTMLResponse, tags=[ "部署成功" ], summary="部署成功" )
async def deploy():
    '''
    部署成功返回信息
    - return: 部署成功
    '''
    html = """
    <div style="text-align:center;margin:0 auto;line-height:500px;">
			<p>部署成功，请按照仓库说明使用</p>
	</div>
    """
    return html


@app.get ( '/favicon.ico', tags=[ "ICO" ], summary="浏览器图标" )
async def favicon():
    '''
    浏览器图标
    - return: ico
    '''
    path = os.path.dirname ( os.path.dirname ( os.path.realpath ( __file__ ) ) )
    favicon_path = path + '/static/ico.jpg'
    return FileResponse ( favicon_path )


@app.get ( "/all", tags=[ "博客信息" ], summary="博客所有文章信息" )
async def all(url: str = '博客地址'):
    '''
    获取博客所有文章信息
    - url: 博客url
    - return: title、link、time组成的一个列表字典
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '博客地址为' + url )
    title_link_time_list = await run_api ( url )
    return title_link_time_list


@app.get ( "/get_article", response_class=HTMLResponse, tags=[ "博客信息" ], summary="博客单篇文章内容" )
async def get_article(url: str = '文章地址'):
    '''
    获取单篇文章信息
    - url: 文章地址
    - return: 文章内容
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '文章地址为' + url )
    html = by_parsel_replace ( url )
    return html


@app.get ( "/get_baidu_token", tags=[ "百度 token" ], summary="获取百度token" )
async def get_baidu_token(API_Key: str, Secret_Key: str, CODE: str):
    '''
    获取百度token
    - API_Key: 百度账号API_Key
    - Secret_Key: 百度账号Secret_Key
    - CODE: 登录并访问 http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={你的API_Key}&redirect_uri=oob&scope=basic&display=popup
    - return: {'access_token': access_token, 'refresh_token': refresh_token}
    '''
    return baidu_get_token ( API_Key, Secret_Key, CODE )


@app.get ( "/get_baidu_refresh", tags=[ "百度 token" ], summary="刷新百度token" )
async def get_baidu_refresh(API_Key: str, Secret_Key: str, refresh_token: str):
    '''
    通过 refresh_token 刷新百度token
    - API_Key: 百度账号API_Key
    - Secret_Key: 百度账号Secret_Key
    - refresh_token: 百度账号refresh_token
    - return: {'access_token': access_token, 'refresh_token': refresh_token}
    '''
    return baidu_refresh_token ( API_Key, Secret_Key, refresh_token )


@app.get ( "/get_hot_article", tags=[ "博客信息" ], summary="获取文章访问统计信息" )
async def get_hot_articles(url: str, access_token: str = None):
    '''
    获取博客热文统计
    - access_token: 百度分析access_token
    - domain: 博客域名
    - return: 以pv排序返回文章标题、链接、pv、uv、平均时长
    '''
    if access_token == None:
        access_token = getToken ()
    return get_hot_article ( access_token, url )


@app.get ( "/get_visitor_province", tags=[ "博客信息" ], summary="获取博客访客省份统计" )
async def get_visitor_provinces(url: str, access_token: str = None):
    '''
    获取访客省份统计
    - access_token: 百度分析access_token
    - domain: 博客域名
    - return: 博客访客省份的UV
    '''
    if access_token == None:
        access_token = getToken ()
    return get_visitor_province ( access_token, url )


@app.get ( "/get_visitor_counrty", tags=[ "博客信息" ], summary="获取博客访客国家统计" )
async def get_visitor_counrtys(access_token: str, url: str):
    '''
    获取访客国家统计
    - access_token: 百度分析access_token
    - domain: 博客域名
    - return: 博客访客国家的UV
    '''
    return get_visitor_counrty ( access_token, url )


# @app.get ( "/screen", response_class=HTMLResponse, tags=[ "截图" ], summary="截取站点封面" )
# async def screen(url: str = '站点网址'):
#     '''
#     获取网址截图
#     - url: 网址
#     - return: img
#     '''
#     if 'http' not in url[ 0:4 ]:
#         url = 'https://' + url
#     print ( '网址为' + url )
#     base64 = save_img ( url )
#     html = f'<img src="data:image/png;base64,{base64}" />'
#     return html


@app.get ( "/csdn", response_class=HTMLResponse, tags=[ "CSDN" ], summary="获取CSDN单篇文章信息" )
async def spider_csdn(url: str = 'CSDN文章地址'):
    '''
    爬取CSDN（仅粉丝可见也可爬取）
    - url: CSDN文章链接
    - return: CSDN文章内容
    '''
    if 'http' not in url[ 0:4 ]:
        url = 'https://' + url
    print ( '网址为' + url )
    html = csdn ( url )
    return html


@app.get ( "/github_calendar", tags=[ "自用转载" ], summary="获取Github贡献信息,url/github_calendar?name" )
async def get_calendars(request: Request):
    '''
    获取Github贡献信息
    - name: Github用户名
    - return: Github Json数据
    '''
    name = str ( request.url ).split ( '?' )[ 1 ]
    return get_calendar ( name )


@app.get ( "/weibo", tags=[ "自用转载" ], summary="获取微博热搜" )
async def get_calendars():
    '''
    获取微博热搜
    - return: 微博 Json数据
    '''
    return get_weibo ()


if __name__ == '__main__':
    uvicorn.run ( "index:app", host="0.0.0.0", reload=True )
    # uvicorn.run (app, host="0.0.0.0" )
    # uvicorn index:app --reload
