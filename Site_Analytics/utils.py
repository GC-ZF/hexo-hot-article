"""
@Author:张时贰
@Date:2022年11月17日
@CSDN:张时贰
@Blog:zhangshier.vip
"""

from enum import Enum

# 百度统计
# 百度统计控制台：https://tongji.baidu.com/main/overview/10000458367/source/all
# 百度统计API文档：https://tongji.baidu.com/api/manual/
class Baidu_Parameter ( Enum ):
    Domain = 'zhangshier.vip'  # 博客的域名
    API_Key = ''
    Secret_Key = ''
    Acess_Token = ''
    Refresh_Token = ''


# 51la统计
class la51_Parameter:
    accessKey = ""
    secretKey = ""
    maskId = ""
