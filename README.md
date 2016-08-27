# PyWebservice

## 为 AhutCourse_mobile 写的后台登陆解析

**描述**

系统使用`python-flask`web框架
模拟登陆网站并解析`html`数据，生成`json`格式数据并返回供移动端使用

*曾挂载在新浪云平台调试并使用*

**技术实现**

* 使用`http`进行模拟登陆，使用 python 的第三方库`requests`
* `GET`、`POST`方法获取目的网页`html`或者`json`信息
* 使用`BeautifulSoup4`解析`requests`下载的网页信息或者使用`json`解析返回信息
* `MySQLdb` ==>> `PyMysql` 使用