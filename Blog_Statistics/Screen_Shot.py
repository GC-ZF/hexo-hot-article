# 因为vercel不支持selenium，此文件全部注释
# import os
# import parsel
# import requests
# from selenium import webdriver
#
#
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
# def save_img(url):
#     # # 先判断并创建文件夹
#     # path = os.path.dirname ( os.path.dirname ( os.path.realpath ( __file__ ) ) )
#     # path = path + '\\resource'
#     # if not os.path.exists ( path ):
#     #     os.mkdir ( path )
#     #
#     # # 获取网页标题作为图片文件名字
#     # request = requests.get ( url ).text
#     # select = parsel.Selector ( request )
#     # title = select.css ( 'title::text' ).get ()
#     # path = f"{path}/{title}.png"
#     # print ( path )
#
#     # 截图
#     # driver = webdriver.Chrome ( options=add_options () )
#     driver = webdriver.Chrome ( options=add_options (),executable_path='static/chromedriver' )
#     driver.maximize_window ()
#     driver.set_page_load_timeout ( 10 )  # 设置超时时间，selenium执行策略是待页面加载完成才执行操作
#     try:
#         driver.get ( driver.get ( url ) )
#     except:  # 捕获timeout异常
#         driver.execute_script ( 'window.stop()' )  # 执行Javascript来停止页面加载 window.stop()
#     # driver.get_screenshot_as_file ( path )  # 保存本地路径
#     base64 = driver.get_screenshot_as_base64 ()  # 为vercel api返回base64
#     driver.quit ()
#     return base64
#
#
# if __name__ == '__main__':
#     url = "https://zhsher.cn/"
#     save_img ( url )
