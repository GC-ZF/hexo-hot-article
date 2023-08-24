import os
import leancloud
import requests


class UpdateAccessToken:
    def __init__(self):
        # Github Action
        self.api_key = os.environ[ "APIKEY" ]  # 百度 API Key
        self.secret_key = os.environ[ "SECRETKEY" ]  # 百度 Secret Key
        # Vercel Environment
        self.app_id = os.environ[ "APPID" ]  # LeanCloud AppID
        self.app_key = os.environ[ "APPKEY" ]  # LeanCloud AppKey

        leancloud.init ( self.app_id, self.app_key )
        self.token = leancloud.Object.extend ( 'BaiduToken' )
        self.query = self.token.query

    def get_token(self):
        '''
        从Leancloud读取token和refreshtoken
        :return:
        '''
        self.query.select ( 'accessToken', 'refreshToken' )
        token_data = self.query.first ()
        self.object_id = token_data.get ( 'objectId' )  # LeanCloud ID
        self.access_token = token_data.get ( 'accessToken' )  # 百度统计 Access Token
        self.refresh_token = token_data.get ( 'refreshToken' )  # 百度统计 Refresh Token

    def update_token(self):
        '''
        更新token
        :return:
        '''
        url = 'http://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token=' \
              + self.refresh_token + '&client_id=' + self.api_key + '&client_secret=' + self.secret_key
        response = requests.get ( url )
        result = response.json ()
        try:
            self.access_token = result[ 'access_token' ]
            self.refresh_token = result[ 'refresh_token' ]
            delete = self.token.create_without_data ( self.object_id )
            delete.destroy ()
            save = self.token ()
            save.set ( 'accessToken', self.access_token )
            save.set ( 'refreshToken', self.refresh_token )
            save.save ()
        except:
            pass
def getToken():
    '''
    为index.py提供读取leancloud函数
    :return: 百度access_token
    '''
    # 通过 LeanCloud 获取百度统计 Access Token
    app_id = os.environ[ "APPID" ]  # LeanCloud AppID
    app_key = os.environ[ "APPKEY" ]  # LeanCloud AppKey
    leancloud.init ( app_id, app_key )
    token = leancloud.Object.extend ( 'BaiduToken' )
    query = token.query
    query.select ( 'accessToken' )
    token_data = query.first ()
    access_token = token_data.get ( 'accessToken' )  # 百度统计 Access Token
    return access_token

if __name__ == '__main__':
    u = UpdateAccessToken ()
    u.get_token ()
    u.update_token ()
