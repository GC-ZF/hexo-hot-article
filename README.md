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

* 百度好请求，但是没文章题目，需要借助爬虫曲爬取，接口太多且有的不能用，好的接口得付费（不过可以自己手撕计算时间/排序文章热度），且token只有一个月的有效期，需要手动填写新的！受访页面统计是以UV从高到低的前20条数据问题不算大，显示一部分文章就可以了，额外数据需要开通企业版
* 51la相对于百度，有文章题目，接口只有6个，比百度目的性强，Json数据清晰。但是请求体需要`accesskey、nonce、secretkey、时间戳`利用SHA256HEX生成 sign（签名），之后将五个参数作为请求体再去请求，十分麻烦。致命的是接口调用次数100/月，想要开通企业版，加客服根本不鸟我，一定要使用可以利用Github工作流实现，但是这样不能保证实时数据

综合考虑，使用百度统计实现文章排行及访客地图。效果：[阅读排行](https://zhangshier.vip/hot-article)

<div align="center">
  <img height="300px" src="https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article06.png">
  <img height="300px" src="https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article07.png">
</div>


## 开通百度统计数据API

参照[Butterfly 安裝文檔(四) 主題配置-2 | Butterfly](https://butterfly.js.org/posts/ceeb73f/#分析統計)，安装注册百度统计服务

![hexo-hot-article 实时文章排行及访客地图05](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article05.png)

百度统计可以获取20条高访问页面数据，为了保证数据的有效性，我在代码中过滤掉了`localhost:4000`以及`tag`、`categories`等页面。为了获取更多的有效数据，可以预先设置不统计`localhost`

**使用设置->规则设置->过滤规则设置**

![hexo-hot-article 实时文章排行及访客地图08](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article08.png)

在百度统计首页中的数据管理，获取`API Key`、`Secrect Key`

访问并登录`http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=oob&scope=basic&display=popup`，获取code，其中`{CLIENT_ID}`替换为`API Key`

![hexo-hot-article 实时文章排行及访客地图01](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article01.png)

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
    var token = '' //百度统计token
    var url = 'zhangshier.vip'	//站点地址
    var api = ''  //hexo-hot-article api 自建或者用我的 https://hexo-hot-article.zhangshier.vip/
    var background = ''  //文章表格鼠标悬停背景色，默认爷爷红
</script>
<link rel="stylesheet" type="text/css"
    href="//cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css">
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hot-article.min.css">
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.1/dist/echarts.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@4.9.0/map/js/china.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hot-article.min.js"></script>
```

hexo三连通过 **『http://localhost:4000/hot-article』** 访问

## 自建API（可选）

接口文档：[hexo-hot-article docs](https://hexo-hot-article.zhangshier.vip/docs)，其中包括获取及刷新百度token的接口、文章发布时间统计接口等

### Vercel一键部署

首先用你的GitHub账号注册：[Vercel](https://vercel.com/)（有账号跳过此步）

点击此处[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-https://github.com/GC-ZF/hexo-hot-article)跳转，对此仓库命名并创建

![hexo-hot-article 实时文章排行及访客地图02](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article02.png)

部署成功后，你会看到 **『部署成功，请按照仓库说明使用』**

![hexo-hot-article 实时文章排行及访客地图03](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article03.png)

上图中右侧的免费域名是被墙的，推荐在 **『setting->domains』** 中绑定一个自己的域名

![hexo-hot-article 实时文章排行及访客地图04](https://testingcf.jsdelivr.net/gh/GC-ZF/hexo-hot-article/static/hexo-hot-article04.png)

### Docker一键部署

启动镜像

```docker
docker run -itd --name=hexo-hot-article --restart=always -v /home/ubuntu/hexo-hot-article:/app/data -p 9135:8000 zhshier/hexo-hot-article
```

测试：返回 **『部署成功，请按照仓库说明使用』** 则部署成功

```
curl http://127.0.0.1:9135
```

在服务器面板中打开9135端口外网即可通过 **『ip:9135』** 访问

## 计划

未来可能添加的功能（先画大饼嘻嘻，应该也发现了最近小张发文频率不高，因为实在是事情太多，近几个月尽量每月一篇吧！）

- [ ] 添加51la、谷歌分析（51la得Github Actions很头痛，数据不能实时更新）

- [ ] 文章发布时间柱状统计图

- [x] 避免重复造轮子部署，自用整合微博、贡献日历

  [Eurkon/weibo-top-api: 使用python爬取微博热搜](https://github.com/Eurkon/weibo-top-api)

  [Zfour/python_github_calendar_api: 用python获取github上的用户贡献信息，部署于vercel的api](https://github.com/Zfour/python_github_calendar_api/)

感谢[@Eurkon](https://github.com/Eurkon)、[@Zfour](https://github.com/Zfour)

如果你有好的点子，多多pr啊🤩
