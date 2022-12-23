"""
@Author:张时贰
@Date:2022年11月16日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
import datetime
import json
import os
import re
from lxml import etree

import requests

'''
百度统计API文档：https://tongji.baidu.com/api/manual/
ACESS_TOKEN 与 REFRESH_TOKEN 申请，查看API文档或以下说明

申请 token 的方法：
    1.在百度统计控制台点击数据管理开通数据并获取 `API Key` 与 `Secret Key`
    2.登录百度账号，获取 `code`（一次性且10min有效） ：http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=oob&scope=basic&display=popup
      其中 `{CLIENT_ID}` 为API key
    3.获取 `ACCESS_TOKEN` ：http://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={CODE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri=oob
      其中 `{CLIENT_ID}`填写您的API Key
          `{CLIENT_SECRET}`填写您的Secret Key
          `{CODE}`填写刚才拿到的CODE
如果你对文档不清楚如何拿到 token 可以借助此项目接口
'''


def baidu_get_token(API_Key, Secret_Key, CODE):
    '''
    获取百度token
    :param API_Key: 百度账号API_Key
    :param Secret_Key: 百度账号Secret_Key
    :param CODE: 登录并访问 http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={你的API_Key}&redirect_uri=oob&scope=basic&display=popup
    :return: {'access_token': access_token, 'refresh_token': refresh_token}
    '''
    payload = {
        "grant_type": "authorization_code",
        "redirect_uri": "oob",
        "code": f'{CODE}',
        "client_id": f'{API_Key}',
        "client_secret": f'{Secret_Key}',
    }
    r = requests.post ( 'http://openapi.baidu.com/oauth/2.0/token', params=payload )
    getData = r.json ()
    try:
        access_token = getData[ 'access_token' ]  # 有效期一个月
        refresh_token = getData[ 'refresh_token' ]  # 有效期十年
        print ( 'Acess_Token：' + '\n' + access_token )
        print ( 'Refresh_Token：' + '\n' + refresh_token )
        token = {'access_token': access_token, 'refresh_token': refresh_token}
        return token
    except Exception as e:
        e = str ( e )
        e = e + '获取失败，请保证code有效（十分钟有效期且仅能使用一次）'
        return e


def baidu_refresh_token(API_Key, Secret_Key, refresh_token):
    '''
    通过 refresh_token 刷新
    :param API_Key: 百度账号API_Key
    :param Secret_Key: 百度账号Secret_Key
    :param refresh_token: 百度账号refresh_token
    :return: {'access_token': access_token, 'refresh_token': refresh_token}
    '''
    payload = {'grant_type': 'refresh_token',
               'refresh_token': refresh_token,
               'client_id': API_Key,
               'client_secret': Secret_Key
               }
    r = requests.post ( 'http://openapi.baidu.com/oauth/2.0/token', params=payload )
    token = r.json ()
    try:
        access_token = token[ 'access_token' ]  # 有效期一个月
        refresh_token = token[ 'refresh_token' ]  # 有效期十年
        print ( "Token更新\nAcess_Token = " + access_token + "\nRefresh_Token = " + refresh_token )
        token = {'access_token': access_token, 'refresh_token': refresh_token}
        return token
    except Exception as e:
        e = str ( e )
        return '错误信息：刷新后无' + e + '值 ， 请检查 refresh_token 是否填写正确'


def getSiteList(access_token, domain):
    '''
    请求获取百度账号下所有的站点列表并处理得到自己博客的 site_id
    :param access_token: 百度分析access_token
    :param domain: 站点域名
    :return: 构造 site_info 字典作为其它请求的 params
    '''
    payload = {'access_token': access_token}
    r = requests.post ( 'https://openapi.baidu.com/rest/2.0/tongji/config/getSiteList', params=payload )
    get_data = r.json ()
    # 多个站点会返回多个 域名 和 id
    # 成功示例：{'list': [{'site_id': 17960579, 'domain': 'zhangshier.vip', 'status': 0, 'create_time': '2022-05-12 15:20:32', 'sub_dir_list': []}]}
    # 失败示例：{'error_code': 110, 'error_msg': 'Access token invalid or no longer valid'}
    # 利用 dic 对站点提取必要的 payload
    getData = get_data[ 'list' ]
    now = datetime.datetime.now ().date ()
    now = datetime.datetime.strftime ( now, '%Y%m%d' )  # 纯字符串格式
    site_info = {}  # 定义一个字典，作为 post 请求的 payload
    for i in getData:
        if i[ 'domain' ].__eq__ ( domain ):
            site_info[ 'site_id' ] = i[ 'site_id' ]
            site_info[ 'domain' ] = i[ 'domain' ]
            site_info[ 'status' ] = i[ 'status' ]
            site_info[ 'start_date' ] = i[ 'create_time' ]
            site_info[ 'end_date' ] = now
    return site_info


def get_hot_article(access_token, domain):
    '''
    获取热文统计
    :param access_token: 百度分析access_token
    :param domain: 站点域名
    :return: 以pv排序返回文章标题、链接、pv、uv、平均时长
    '''
    site_info = getSiteList ( access_token, domain )  # 站点基础数据
    payload = {
        'access_token': access_token,
        'method': 'visit/toppage/a',
        "metrics": "pv_count,visitor_count,average_stay_time",  # 浏览量 访客数 平均访问时长s
    }
    payload.update ( site_info )
    r = requests.post ( 'https://openapi.baidu.com/rest/2.0/tongji/report/getData', params=payload )
    get_site_data = r.json ()

    # 对 get_site_data 二次处理，去除主页、友链朋友圈、关于等信息，只保留 post 文章页信息
    # 并构造一个字典 get_hot_article 包括 概览信息blog_general 每篇文章信息article_info
    # 文章概览信息
    blog_general = {"timeSpan": get_site_data[ 'result' ][ 'timeSpan' ][ 0 ],  # 统计时间区间 eg：2022/05/12 - 2022/11/17
                    "total": get_site_data[ 'result' ][ 'total' ],  # 百度统计控制台-受访页面中URL个数 但只有前20篇具体数据，需要购买商业版统计
                    "sum_pv_count": get_site_data[ 'result' ][ 'sum' ][ 0 ][ 0 ],  # 总浏览量 PV
                    "sum_visitor_count": get_site_data[ 'result' ][ 'sum' ][ 0 ][ 1 ],  # 总访客数 UV
                    "sum_average_stay_time": get_site_data[ 'result' ][ 'sum' ][ 0 ][ 2 ],  # 总平均停留时长 单位 s
                    "top20_pv_count": get_site_data[ 'result' ][ 'pageSum' ][ 0 ][ 0 ],  # 前20篇的总浏览量 PV
                    "top20_visitor_count": get_site_data[ 'result' ][ 'pageSum' ][ 0 ][ 1 ],  # 前20篇的总访客数 UV
                    "top20_average_stay_time": get_site_data[ 'result' ][ 'pageSum' ][ 0 ][ 2 ],  # 前20篇的平均访问时长
                    # 前20篇的总平均停留时长 单位 s
                    }

    post_num = len ( get_site_data[ 'result' ][ 'items' ][ 0 ] )  # 避免有的人文章少超出索引

    # 去除主页、友链朋友圈、关于等信息，只保留 post 文章页信息
    index = 0
    for i in range ( 0, post_num ):
        if not re.match ( r'^https://' + site_info[ 'domain' ] + '/post/*',
                          get_site_data[ 'result' ][ 'items' ][ 0 ][ i - index ][ 0 ][ 'name' ] ):
            del get_site_data[ 'result' ][ 'items' ][ 0 ][ i - index ]
            del get_site_data[ 'result' ][ 'items' ][ 1 ][ i - index ]
            index = index + 1
    post_num = len ( get_site_data[ 'result' ][ 'items' ][ 0 ] )  # 去除处理后更新

    # 单篇文章信息 百度统计没title：利用 xpath 爬取博客获取文章标题
    article_info = [ ]
    for i in range ( 0, post_num ):
        tmp = {"title": get_title ( get_site_data[ 'result' ][ 'items' ][ 0 ][ i ][ 0 ][ 'name' ] ),
               "url": get_site_data[ 'result' ][ 'items' ][ 0 ][ i ][ 0 ][ 'name' ],  # 文章链接
               "pv_count": get_site_data[ 'result' ][ 'items' ][ 1 ][ i ][ 0 ],  # 浏览量PV
               "visitor_count": get_site_data[ 'result' ][ 'items' ][ 1 ][ i ][ 1 ],  # 访客数UV
               "average_stay_time": get_site_data[ 'result' ][ 'items' ][ 1 ][ i ][ 2 ]  # 平均停留时长
               }
        article_info.append ( tmp )

    # 构造新字典并return
    get_hot_article = {"blog_general": blog_general, "article_info": article_info}

    # pwd = os.getcwd ()
    # father_path_method1 = os.path.dirname ( pwd )
    # file_path = father_path_method1 + "\\baidu.json"
    # with open ( file_path, 'w', encoding='utf-8' ) as f:
    #     json.dump ( get_post_data, f, indent=4, ensure_ascii=False )
    return get_hot_article


def get_title(url):
    '''
    补充百度分析不显示标题
    :param url: 文章链接
    :return: 文章标题
    '''
    r = requests.get ( url )
    r = r.content.decode ( 'utf-8' )
    html = etree.HTML ( r )
    title = html.xpath ( '//*[@id="post-info"]/h1//text()' )[ 0 ]
    return title


def get_visitor_province(access_token, domain):
    '''
    访客省份统计
    :param access_token: 百度分析access_token
    :param domain: 站点域名
    :return: 省份UV
    '''
    site_info = getSiteList ( access_token, domain )  # 站点基础数据
    payload = {
        'access_token': access_token,
        'method': 'overview/getDistrictRpt',
        "metrics": "pv_count",  # 获取pv_count或visitor_count
    }
    payload.update ( site_info )
    r = requests.post ( 'https://openapi.baidu.com/rest/2.0/tongji/report/getData', params=payload )
    get_data = r.json ()
    print ( get_data[ 'result' ][ 'items' ][ 0 ] )
    print ( get_data[ 'result' ][ 'items' ][ 1 ] )
    get_visitor_province = [ ]
    num = len ( get_data[ 'result' ][ 'items' ][ 0 ] )
    for i in range ( 0, num ):
        # get_data[ 'result' ][ 'items' ][ 1 ][ i ][ 0 ] # PV
        tmp = {'name': get_data[ 'result' ][ 'items' ][ 0 ][ i ],
               'value': get_data[ 'result' ][ 'items' ][ 1 ][ i ][ 0 ]}
        get_visitor_province.append ( tmp )
    return get_visitor_province


def get_visitor_counrty(access_token, domain):
    '''
    访客国家统计
    :param access_token: 百度分析access_token
    :param domain: 站点域名
    :return: 国家UV
    '''
    site_info = getSiteList ( access_token, domain )  # 站点基础数据
    payload = {
        'access_token': access_token,
        'method': 'visit/world/a',
        "metrics": "pv_count,visitor_count,average_stay_time",  # 浏览量 访客数 平均访问时长s
    }
    payload.update ( site_info )
    r = requests.post ( 'https://openapi.baidu.com/rest/2.0/tongji/report/getData', params=payload )
    get_data = r.json ()
    get_visitor_country = [ ]
    num = len ( get_data[ 'result' ][ 'items' ][ 0 ] )
    for i in range ( 0, num ):
        # get_data[ 'result' ][ 'items' ][ 0 ] # 国家
        # get_data[ 'result' ][ 'items' ][ 1 ][ i ][ 0 ] # PV
        # get_data[ 'result' ][ 'items' ][ 1 ][ i ][ 1 ] # UV
        tmp = {'name': get_data[ 'result' ][ 'items' ][ 0 ][ i ][ 0 ][ 'name' ],
               'value': get_data[ 'result' ][ 'items' ][ 1 ][ i ][ 0 ]}
        get_visitor_country.append ( tmp )
    return get_visitor_country


if __name__ == '__main__':
    API_Key = ''
    Secret_Key = ''
    CODE = ''
    refresh_token = ''
    # 测试
    # print ( baidu_get_token ( API_Key, Secret_Key, CODE ) )
    # print ( baidu_refresh_token ( API_Key, Secret_Key, refresh_token ) )

    # access_token = ''
    # domain = 'zhangshier.vip'
    # print ( get_hot_article ( access_token, domain ) )
    # print ( get_visitor_province ( access_token, domain ) )
    # print ( get_visitor_counrty ( access_token, domain ) )
