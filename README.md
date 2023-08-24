<h1 align="center">hexo-hot-article</h1>

<!-- 徽标 -->
<p align="center">
  <a href="https://github.com/GC-ZF/hexo-hot-article/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/GC-ZF/hexo-hot-article" alt="license">
  </a>

  <img src="https://img.shields.io/badge/python-3.7.3+-blue" alt="python">

  <a style="margin-inline:5px" target="_blank" href="">
    <img  src="https://visitor-badge.glitch.me/badge?page_id=hexo-hot-article" title="访客"/>
  </a>
</p></br>

## 前言

灵感来源于[@二花 阅读排行](https://thiscute.world/statistics/)

关于网站统计平台的选择，第一想到的也是51la，我深度使用的感受

* 百度好请求，但是没文章题目，需要借助爬虫曲爬取，接口太多且有的不能用，好的接口得付费（不过可以自己手撕计算时间/排序文章热度），且token只有一个月的有效期，需要手动填写新的（已解决）！受访页面统计是以UV从高到低的前20条数据问题不算大，显示一部分文章就可以了，额外数据需要开通企业版
* 51la相对于百度，有文章题目，接口只有6个，比百度目的性强，Json数据清晰。但是请求体需要`accesskey、nonce、secretkey、时间戳`利用SHA256HEX生成 sign（签名），之后将五个参数作为请求体再去请求，十分麻烦。致命的是接口调用次数100/月，想要开通企业版，加客服根本不鸟我，一定要使用可以利用Github工作流实现，但是这样不能保证实时数据

综合考虑，使用百度统计实现文章排行及访客地图。效果：[阅读排行](https://zhsher.cn/hot-article)

<div align="center">
  <img height="300px" src="https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article01.png">
  <img height="300px" src="https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article02.png">
</div>

## 开通百度统计数据API

参照[Butterfly 安裝文檔(四) 主題配置-2 | Butterfly](https://butterfly.js.org/posts/ceeb73f/#分析統計)，安装注册百度统计服务

![hexo-hot-article 实时文章排行及访客地图03](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article03.png)

百度统计可以获取20条高访问页面数据，为了保证数据的有效性，我在代码中过滤掉了`localhost:4000`以及`tag`、`categories`等页面。为了获取更多的有效数据，可以预先设置不统计`localhost`

**使用设置->规则设置->过滤规则设置**

![hexo-hot-article 实时文章排行及访客地图04](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article04.png)

在百度统计首页中的数据管理，获取`API Key`、`Secrect Key`

访问并登录`http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=oob&scope=basic&display=popup`，获取code，其中`{CLIENT_ID}`替换为`API Key`

![hexo-hot-article 实时文章排行及访客地图05](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article05.png)

访问`http://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={你的CODE}&client_id={你的API Key}&client_secret={你的Secrect Key}&redirect_uri=oob`，获取token

## 引入博客

新建一个页面

```shell
hexo new page hot-article
```

生成`source/hot-article/index.md` 文件，打开该文件，粘贴以下内容：

```html
<div id='hexo-hot-article'></div>
<div id='hexo-china-map' style="height: 500px;"></div>
<script>
    var token = '' //百度统计token vercel自建请留空
    var url = 'zhsher.cn'	//站点地址
    var api = ''  //hexo-hot-article api 留空默认使用 https://hexo-hot-article.zhsher.cn/ 自建使用自己的接口
    var background = ''  //文章表格鼠标悬停背景色，留空默认爷爷红
</script>
<link rel="stylesheet" type="text/css"
      href="//cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css">
<link rel="stylesheet" type="text/css" href="https://jsd.onmicrosoft.cn/gh/GC-ZF/hexo-hot-article/static/hot-article.min.css">
<script type="text/javascript" src="https://jsd.onmicrosoft.cn/gh/GC-ZF/hexo-hot-article/static/hot-article.min.js"></script>
<script src="https://jsd.onmicrosoft.cn/npm/echarts@5.4.1/dist/echarts.js"></script>
<script type="text/javascript" src="https://jsd.onmicrosoft.cn/npm/echarts@4.9.0/map/js/china.js"></script>
```

hexo三连通过 **『http://localhost:4000/hot-article』** 访问

## 自建项目（可选）

为了解决百度token只有一个月需要手动更新痛点，借鉴[Hexo 博客实时访问统计图 | Eurkon](https://blog.eurkon.com/post/61763977.html)的文章，使用同样的原理实现

使用 Github + LeanCloud + Vercel，整个部署均在云端完成。运行原理：

1. 数据存储在 LeanCloud 数据库，也可以自行修改源码存储在其他数据库；
2. 通过 Github Action 更新百度统计的 `AccessToken` 和 `RefreshToken`；
3. Vercel 部署的 API 从 LeanCloud 获取 `AccessToken`，再执行请求，获取百度统计数据，返回给前端。

接口文档：[hexo-hot-article docs](https://hexo-hot-article.zhsher.cn/docs)，其中包括获取及刷新百度token的接口、文章发布时间统计接口等

### LeanCloud数据库配置

新建结构化数据，创建 Class，填写名称为 `BaiduToken`，设置默认 ACL read 和 write 权限都为所有用户；

![hexo-hot-article 实时文章排行及访客地图06](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article06.png)

点击添加列，分别新增 `accessToken` 和 `refreshToken`；

![hexo-hot-article 实时文章排行及访客地图07](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article07.png)

点击新增行，填写百度统计获取到的 `access_token` 和 `refresh_token`；

点击**设置-->应用凭证**获取连接LeanCloud的`APPID`与`APPKey`

![hexo-hot-article 实时文章排行及访客地图08](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article08.png)

### Github部署

fork [GC-ZF/hexo-hot-article](https://github.com/GC-ZF/hexo-hot-article) 项目， `Settings-->Security>-->Secrets>-->Actions` 中添加以下秘钥：

- `APIKEY`： 百度统计 API Key
- `SECRETKEY`：百度统计 Secret Key
- `APPID`：LeanCloud AppID
- `APPKEY`：LeanCloud AppKey

![hexo-hot-article 实时文章排行及访客地图09](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article09.png)

点击`Backup twikoo-->Enable workflow`启用工作流，然后点击`Run workflow`手动运行测试能否运行并更新leancloud中的token

![hexo-hot-article 实时文章排行及访客地图10](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article10.png)

### Vercel一键部署

将自己fork的项目导入Vercel并设置环境变量

![hexo-hot-article 实时文章排行及访客地图11](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article11.png)

部署成功后，你会看到 **『部署成功，请按照仓库说明使用』**

![hexo-hot-article 实时文章排行及访客地图12](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article12.png)

上图中右侧的免费域名是被墙的，推荐在 **『setting->domains』** 中绑定一个自己的域名

![hexo-hot-article 实时文章排行及访客地图13](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article13.png)

### Docker一键部署

vercel也可以使用Docker替代

启动镜像

```docker
docker run -itd --name=hexo-hot-article --restart=always -v /home/ubuntu/hexo-hot-article:/app/data -p 9135:8000 -e APPID="LeanCloud的APPID" -e APPKEY="LeanCloud的APPKEY" -zhshier/hexo-hot-article
```

测试：返回 **『部署成功，请按照仓库说明使用』** 则部署成功

```
curl http://127.0.0.1:9135
```

在服务器面板中打开9135端口外网即可通过 **『ip:9135』** 访问

## 更新

未来可能添加的功能（先画大饼嘻嘻，应该也发现了最近小张发文频率不高，因为实在是事情太多，近几个月尽量每月一篇吧！）

- [x] 2023.08.24vercel自建添加自动更新百度token

- [x] 2023.01.26避免重复造轮子部署，自用整合微博、贡献日历

  [Eurkon/weibo-top-api: 使用python爬取微博热搜](https://github.com/Eurkon/weibo-top-api)

  [Zfour/python_github_calendar_api: 用python获取github上的用户贡献信息，部署于vercel的api](https://github.com/Zfour/python_github_calendar_api/)

- [ ] 添加51la、谷歌分析（51la得Github Actions很头痛，数据不能实时更新）

- [ ] 文章发布时间柱状统计图

感谢[@Eurkon](https://github.com/Eurkon)、[@Zfour](https://github.com/Zfour)

如果你有好的点子，多多pr啊🤩
