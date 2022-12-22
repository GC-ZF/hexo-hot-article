import requests
import string
import random
import time
import json
import hashlib

# pip install pycryptodome
from Site_Analytics.utils import la51_Parameter


def sha256Hex(dist_param, common_param):
    sign_str = "accessKey=" + common_param[ "accessKey" ] + "&nonce=" + dist_param[ "nonce" ] + "&secretKey=" + \
               common_param[ "secretKey" ] + "&timestamp=" + str ( dist_param[ "timestamp" ] )
    return str ( hashlib.sha256 ( sign_str.encode ( "utf8" ) ).hexdigest () ).upper ()


headers = {
    "Content-Type": "application/json"
}
common_param = {
    # 请在此处填入您的accessKey
    "accessKey": la51_Parameter.accessKey.vale,
    # 请在此处填入您的secretKey
    "secretKey": la51_Parameter.secretKey.vale,
    # 请在此处填入您的maskId
    "maskId": la51_Parameter.maskId.vale
}
nonce = random.sample ( string.ascii_letters + string.digits, 4 )
timestamp = int ( time.time ()*1000 )
param = {
    "accessKey": common_param[ "accessKey" ],
    "nonce": ''.join ( nonce ),
    "timestamp": timestamp,
    "maskId": common_param[ "maskId" ]
}
param[ "sign" ] = sha256Hex ( param, common_param )
result = requests.post ( url="https://v6-open.51.la/open/overview/get", data=json.dumps ( param ), headers=headers )
if result.status_code == 200:
    print ( result.text )  # 中、低等安全性校验情况下直接返回数据
