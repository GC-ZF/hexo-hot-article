function hotarticle() {
	fetch(article_api).then(res => res.json()).then((data) => { //获取博客文章排行
		var c = document.querySelectorAll('#hexo-hot-article')[0]

		var blog_general = data['blog_general'] //总的信息
		var article_info = data['article_info'] //单篇文章信息

		var table_general = document.createElement('table'); //建表存总的信息
		table_general.id = 'hot-sum'
		var table_article = document.createElement('table'); //建表存单篇文章信息
		table_article.id = 'hot-article'

		var sencond = blog_general['sum_average_stay_time'] * blog_general['sum_visitor_count']
		let time = getTime(sencond)

		// 第一个表
		table_general.innerHTML = `
				<thead>
					<tr>
						<th>起始时间</th>
						<th>总访客数 UV</th>
						<th>总访问量 PV</th>
						<th>总阅读时长</th>
						<th>人均阅读时长</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td class="score">${blog_general['timeSpan']}</td>
						<td class="score">${blog_general['sum_visitor_count']}</td>
						<td class="score">${blog_general['sum_pv_count']}</td>
						<td class="score">${time[0]}时${time[1]}分${time[2]}秒</td>
						<td class="score">${blog_general['sum_average_stay_time']}</td>
					</tr>
				</tbody>
				`

		// 第二个表
		table_article.innerHTML = `
					<thead>
						<tr>
							<th class="sort-table" data-type="number">Num</th>
							<th class="sort-table" data-type="string">Title</th>
							<th class="sort-table" data-type="number">PV</th>
							<th class="sort-table" data-type="number">UV</th>
							<th class="sort-table" data-type="number">Average Time</th>
						</tr>
					</thead>`
		tbody = document.createElement('tbody');
		tbody.id = 'list';
		for (let i = 0; i < article_info.length; i++) {
			var tr = document.createElement('tr');
			tr.innerHTML += `
							<td class="score">${i+1}</td>
							<td class="score"><a href=${article_info[i]['url']}>${article_info[i]['title']}</a></td>
							<td class="score">${article_info[i]['pv_count']}</td>
							<td class="score">${article_info[i]['visitor_count']}</td>
							<td class="score">${article_info[i]['average_stay_time']}</td>
						`
			tbody.appendChild(tr);
		}
		table_article.appendChild(tbody);
		var table_sum_title = document.createElement('h2');
		table_sum_title.innerHTML = `全站统计`
		var table_article_title = document.createElement('h2');
		table_article_title.innerHTML = `阅读排行`
		c.innerHTML = ``
		c.appendChild(table_sum_title);
		c.appendChild(table_general); //第一个表
		c.appendChild(table_article_title);
		c.appendChild(table_article); //第二个表
		sort(); //排序
		// 注册色值
		if (typeof(background) == "undefined" || background == null || background == '') {
			// console.log('未设置色值')
		} else {
			console.log('已设置色值')
			// setBackground(background);
		}
	});
}

function chinamap() {
	fetch(chinamap_api).then(res => res.json()).then((data) => {
		var X = data;
		var color = document.documentElement.getAttribute('data-theme') === 'light' ? '#405449' :
			'#96a7be' //50绿 10蓝
		// 初始化echarts实例
		// console.log(X)
		var myEcharts = echarts.init(document.getElementById("hexo-china-map"));
		var option = {
			title: { //标题样式
				text: '访客地图',
				x: "center",
				textStyle: {
					fontSize: 18,
					color: color
				},
			},
			tooltip: {
				trigger: 'item',
				formatter: function(params) {
					// console.log(params)
					if (params.name) {
						return params.name + '<br/>UV : ' + (isNaN(params.value) ? 0 : parseInt(params
							.value));
					}
				}
			},
			visualMap: { //视觉映射组件
				top: 'bottom',
				left: 'left',
				min: 10,
				max: 50000,
				// text: ['High', 'Low'],
				realtime: false, //拖拽时，是否实时更新
				calculable: true, //是否显示拖拽用的手柄
				inRange: {
					color: ['lightskyblue', 'yellow', 'orangered']
				}
			},
			series: [{
				name: '访客地图',
				type: 'map',
				mapType: 'china',
				roam: false, //是否开启鼠标缩放和平移漫游
				itemStyle: { //地图区域的多边形 图形样式
					normal: { //是图形在默认状态下的样式
						label: {
							show: true, //是否显示标签
							textStyle: {
								color: "black"
							}
						}
					},
					zoom: 1.5, //地图缩放比例,默认为1
					emphasis: { //是图形在高亮状态下的样式,比如在鼠标悬浮或者图例联动高亮时
						label: {
							show: true
						}
					}
				},
				top: "3%", //组件距离容器的距离
				data: X
			}]
		};
		// 使用刚指定的配置项和数据显示图表。
		myEcharts.setOption(option);
	})
}

// 转换时间
function getTime(time) {
	// 转换为式分秒
	let h = parseInt(time / 60 / 60 % 24)
	h = h < 10 ? '0' + h : h
	let m = parseInt(time / 60 % 60)
	m = m < 10 ? '0' + m : m
	let s = parseInt(time % 60)
	s = s < 10 ? '0' + s : s
	// 作为返回值返回
	return [h, m, s]
}

// 自定义背景颜色
function setBackground(color) {
	var score = document.getElementsByClassName("score");
	for (var i = 0; i < score.length; i++) {
		//注册鼠标进入事件
		score[i].onmouseover = function() {
			this.style.backgroundColor = color;
		};
		//注册鼠标离开事件
		score[i].onmouseout = function() {
			//恢复到这个标签默认的颜色
			this.style.backgroundColor = "";
		};
	}
}

// 表格排序
function sort() {
	'use strict';
	var ths = document.getElementsByClassName("sort-table")
	console.log(ths)
	var i;
	var sortOrder = 1; // 1: 昇順、 -1: 降順
	for (i = 0; i < ths.length; i++) {
		ths[i].addEventListener('click', function() {
			// var rows = document.querySelectorAll('#hot-article tbody > tr'); // NodeList
			var rows = Array.prototype.slice.call(document.querySelectorAll('#hot-article tbody > tr'));
			var col = this.cellIndex;
			var type = this.dataset.type;
			rows.sort(function(a, b) {
				if (type === "number") {
					var _a = a.children[col].textContent * 1;
					var _b = b.children[col].textContent * 1;
				}
				if (type === "string") {
					var _a = a.children[col].textContent.toLowerCase();
					var _b = b.children[col].textContent.toLowerCase();
				}
				if (_a < _b) {
					return -1 * sortOrder;
				}
				if (_a > _b) {
					return 1 * sortOrder;
				}
				return 0;
			});
			var tbody = document.querySelector('#hot-article tbody');
			while (tbody.firstChild) {
				tbody.removeChild(tbody.firstChild);
			}
			var j;
			for (j = 0; j < rows.length; j++) {
				tbody.appendChild(rows[j]);
			}
			var k;
			for (k = 0; k < ths.length; k++) {
				ths[k].className = '';
			}
			this.className = sortOrder === 1 ? 'asc' : 'desc';
			sortOrder *= -1;
		});
	}
};


// 判断是否有接口
if (typeof(api) == "undefined" || api == null || api == '') {
	var article_api = `https://hexo-hot-article.zhangshier.vip/get_hot_article?access_token=${token}&url=${url}`
	var chinamap_api = `https://hexo-hot-article.zhangshier.vip/get_visitor_province?access_token=${token}&url=${url}`
} else {
	var article_api = `${api}get_hot_article?access_token=${token}&url=${url}`
	var chinamap_api = `${api}get_visitor_province?access_token=${token}&url=${url}`
}
if (document.querySelectorAll('#hexo-hot-article')[0]) {
	var c = document.querySelectorAll('#hexo-hot-article')[0]
	c.innerHTML = `<p>文章在路上啦...</p>`
	hotarticle();
}
if (document.getElementById("hexo-china-map")) {
	var c = document.querySelectorAll('#hexo-china-map')[0]
	c.innerHTML = `<p>绘制地图中...</p>`
	chinamap();
};
