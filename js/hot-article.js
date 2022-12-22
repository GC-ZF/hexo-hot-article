if (typeof(api) == "undefined" || api == null) {
	console.log('未填写api')
	var api = `https://test.zhangshier.vip/get_hot_post?access_token=${token}&url=${url}`
} else {
	console.log('已填写api')
	var api = `${api}get_hot_post?access_token=${token}&url=${url}`
}
let c = document.querySelectorAll('#hot_post')[0]
c.innerHTML = `<p>连接中...</p>`
// console.log(api)
fetch(api).then(res => res.json()).then((data) => { //获取博客文章排行


	var post_general = data['post_general'] //总的信息
	var post_info = data['post_info'] //单篇文章信息

	var table_sum = document.createElement('table'); //建表存总的信息
	table_sum.id = 'hot-sum'
	var table_post = document.createElement('table'); //建表存单篇文章信息
	table_post.id = 'hot-post'

	var sencond = post_general['sum_average_stay_time'] * post_general['sum_visitor_count']
	let time = getTime(sencond)

	// 第一个表
	table_sum.innerHTML = `
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
					<td>${post_general['timeSpan']}</td>
					<td>${post_general['sum_visitor_count']}</td>
					<td>${post_general['sum_pv_count']}</td>
					<td>${time[0]}时${time[1]}分${time[2]}秒</td>
					<td>${post_general['sum_average_stay_time']}</td>
				</tr>
			</tbody>
			`

	// 第二个表
	table_post.innerHTML = `
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
	for (let i = 0; i < post_info.length; i++) {
		var tr = document.createElement('tr');
		tr.innerHTML += `
						<td>${i+1}</td>
						<td><a href=${post_info[i]['url']}>${post_info[i]['title']}</a></td>
						<td class="score">${post_info[i]['pv_count']}</td>
						<td class="score">${post_info[i]['visitor_count']}</td>
						<td class="score">${post_info[i]['average_stay_time']}</td>
					`
		tbody.appendChild(tr);
	}
	c.innerHTML = ``
	table_post.appendChild(tbody)
	c.appendChild(table_sum) //第一个表
	c.appendChild(table_post) //第二个表
	sort(); //排序
});

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

function sort() {
	'use strict'; // 厳格なエラーチェック

	// コードが長くなったらリファクタリングする 関数生成

	// 見出しをクリックしたら何かの処理をする
	var ths = document.getElementsByClassName("sort-table")
	console.log(ths)
	var i;
	var sortOrder = 1; // 1: 昇順、 -1: 降順
	for (i = 0; i < ths.length; i++) { // iがths.lengthより小さい間、iを増やしながら次のことをしなさい
		ths[i].addEventListener('click', function() {
			// 何番目の列の見出しがクリックされたかヒ表示する
			// console.log(this.cellIndex); // this.cellIndexで調べる

			// sort
			// var arr = ['taguchi', 'fkoji', 'dotinstall']; // 配列
			// 行要素が入った配列を作成する
			// tbody直下のtr要素を取得する
			// querySelecterAll() セレクタで要素を取得する
			var rows = document.querySelectorAll('#hot-post tbody > tr'); // NodeList
			// NodeListを配列に変換する
			var rows = Array.prototype.slice.call(document.querySelectorAll('#hot-post tbody > tr'));
			// Array.prototype.slice() 配列の一部を取り出して新しい配列を返します
			// console.log(rows);
			// return;

			var col = this.cellIndex; // セルのインデックス番号を取得する
			var type = this.dataset.type; // string, number

			// ある値を取り出して、それを比較する 今回はtd
			rows.sort(function(a, b) { // tr, tr, tr要素が順次渡されていく
				if (type === "number") {
					var _a = a.children[col].textContent * 1;
					var _b = b.children[col].textContent * 1;
				}
				if (type === "string") {
					// tr要素の中にあるtd要素のうち、クリックされた列番目の中身を引っ張ってくる
					var _a = a.children[col].textContent.toLowerCase();
					// 大文字、小文字の区別をなくすために大文字を小文字にする .toLowerCase();  
					// a = tr trの子要素tdを引っ張ってくる this.cellIndexは入れ込めないので変数を定義する var = col
					var _b = b.children[col].textContent.toLowerCase();
				}
				// 降順にするには返り値を逆にする
				if (_a < _b) {
					return -1 * sortOrder;
				}
				if (_a > _b) {
					return 1 * sortOrder;
				}
				return 0;
			});
			// console.log(rows);
			// 配列の並び替え完了
			// rows 並び替えられた配列の要素

			// 表の中身を書き換える
			// tbodyの中身を一旦消す
			// 並び替えられた配列の要素をtbodyの子要素として追加していく



			var tbody = document.querySelector('#hot-post tbody');

			while (tbody.firstChild) { // tbodyの最初の子要素がある限り
				tbody.removeChild(tbody.firstChild); // tbodyの最初の子要素を削除する
				// 最初の子要素が無くなるまで、どんどん消していく
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

			sortOrder *= -1; // クリックしたら反転させる

		});
	}
};
